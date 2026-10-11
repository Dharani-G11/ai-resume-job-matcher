from main import resume_collection


def test_resume_isolation():
    results = resume_collection.get(
        where={"resume_id": 21}
    )

    assert len(results["ids"]) > 0

    for metadata in results["metadatas"]:
        assert metadata["resume_id"] == 21