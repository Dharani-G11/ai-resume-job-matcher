# AI Resume & Job-Match Assistant

An AI-powered application that helps compare a resume with a job description.

The idea behind this project is simple: a user can upload a resume PDF and provide a job description. The application processes the resume, finds the most relevant information for the job, and uses an AI model to generate an analysis.

I built this project to learn and practice backend development with FastAPI and to understand how RAG, embeddings, semantic search, vector databases, PostgreSQL, and local LLMs can work together in a real application.

## What It Does

- Uploads a resume in PDF format
- Extracts text from the PDF
- Splits the resume into smaller text chunks
- Generates embeddings for the resume chunks
- Stores embeddings in ChromaDB
- Stores structured application data in PostgreSQL
- Accepts job descriptions
- Performs semantic search between the job description and resume content
- Retrieves relevant resume sections
- Uses Ollama to generate an AI-based analysis
- Provides the application through FastAPI REST APIs
- Supports Docker-based execution
- Includes tests for different parts of the backend

## How It Works

The basic workflow of the application is:

```text
Resume PDF
    |
    v
Extract Resume Text
    |
    v
Split Text into Chunks
    |
    v
Generate Embeddings
    |
    v
Store Embeddings in ChromaDB
    |
    v
Job Description
    |
    v
Generate Job Description Embedding
    |
    v
Semantic Search
    |
    v
Retrieve Relevant Resume Chunks
    |
    v
Build Context for the LLM
    |
    v
Ollama
    |
    v
Generate AI Resume Analysis
