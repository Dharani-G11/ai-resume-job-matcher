from email.mime import text

import fitz
import chromadb
from ollama import Client
from fastapi import FastAPI ,UploadFile , File , Depends
from sqlalchemy.orm import Session
from fsspec.implementations import data
from google.type import postal_address_pb2
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from database import SessionLocal
from models import Resume, Job , Analysis



from database import Base
app = FastAPI()

ollama_client = Client(
    host="http://host.docker.internal:11434"
)

class JobDescription(BaseModel):
    text: str
    resume_id:int
    {
        "Looking for a Python backend developer with FastAPI and PostgreSQL experience."
    }


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path = "./chroma_db")
resume_collection = chroma_client.get_or_create_collection(name= "resume_chunks")
print("Existing chroma records:",resume_collection.count())

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@app.get("/")
def home():
    return{"message":"AI resume job match API is running"}


@app.get("/test_db")
def db_test(db:Session = Depends(get_db)):
    return {"message":"Database Session Created"}

@app.post("/resume" )
async def upload_resume(
        file: UploadFile = File(...),
        db:Session = Depends(get_db)
):
    contents = await file.read()
    doc = fitz.open(stream=contents,filetype="pdf")
    text = ""

    for page in doc:
        text +=page.get_text()

    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line:
            clean_lines.append(line)
    clean_texts = "\n".join(clean_lines)

    chunk_size = 500
    overlap = 100

    chunks = []
    start = 0
    while start< len(clean_texts):
        chunk = clean_texts [start:start+chunk_size]
        chunks.append(chunk)
        start += chunk_size - overlap

    embeddings = model.encode(chunks)

    resume = Resume(filename=file.filename)

    db.add(resume)
    db.commit()
    db.refresh(resume)

    ids = [
        f"resume_{resume.id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadata = [
        {
            "source": "resume",
            "resume_id": resume.id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    resume_collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

    print(resume_collection.get(
        where={"resume_id": resume.id}
    ))


    print("resume_collection:",resume_collection.count())
    stored_data = resume_collection.get()
    print(stored_data)


    return{
        "resume.id":resume.id,
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embedding_count": len(embeddings),
        "embedding_dimensions":len(embeddings[0])
    }

@app.post("/job-description")
async def job_description(
        data: JobDescription,
        db:Session = Depends(get_db)
):
    job = Job(
        title="Job Description",
        description=data.text
    )

    db.add(job)
    db.commit()
    db.refresh(job)


    job_embedding = model.encode ([data.text])
    results = resume_collection.query(
        query_embeddings=job_embedding.tolist(),
        n_results=3,
        where = {"resume_id": data.resume_id}
    )
    retrieved_chunks = results["documents"][0]

    prompt = f"""
    Analyze the candidate's resume against the job description.

    JOB DESCRIPTION:
    {data.text}

    RELEVANT RESUME INFORMATION:
    {retrieved_chunks}

    TASK:
    Identify matching skills, relevant experience,
    missing requirements, and explain the reasoning.
    """

    response = ollama_client.chat(
        model="qwen2.5:3b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    analysis = Analysis(
        resume_id=data.resume_id,
        job_id=job.id,
        result=response.message.content
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return{
        "job_id":job.id,
        "job_description":data.text,
        "embeddings_dimensions":len(job_embedding[0]),
        "distances": results["distances"][0],
        "metadata": results["metadatas"][0],
        "ai_analysis": response.message.content
    }
