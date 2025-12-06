"""
Test script to verify semantic search is working correctly
Run this to check if ChromaDB is returning relevant results
"""

from utils.database import DatabaseManager

def test_semantic_search():
    print("Testing Semantic Search...")
    print("=" * 50)
    
    # Initialize database
    db = DatabaseManager()
    
    # Clear existing data
    db.clear_collection()
    print("✓ Cleared database")
    
    # Add test documents
    test_docs = [
        {
            "content": "Python is a programming language that is widely used for web development, data science, and automation.",
            "metadata": {"filename": "python_intro.txt", "file_type": "txt"}
        },
        {
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
            "metadata": {"filename": "ml_basics.txt", "file_type": "txt"}
        },
        {
            "content": "The Eiffel Tower is located in Paris, France. It was built in 1889 and is one of the most famous landmarks.",
            "metadata": {"filename": "paris_guide.txt", "file_type": "txt"}
        },
        {
            "content": "Cooking pasta requires boiling water, adding salt, and cooking for 8-12 minutes until al dente.",
            "metadata": {"filename": "cooking_tips.txt", "file_type": "txt"}
        }
    ]
    
    # Add documents
    for doc in test_docs:
        success, msg = db.add_document(doc["content"], doc["metadata"])
        if success:
            print(f"✓ Added: {doc['metadata']['filename']}")
        else:
            print(f"✗ Failed: {msg}")
    
    print("\n" + "=" * 50)
    print("Running Test Queries...")
    print("=" * 50 + "\n")
    
    # Test queries
    test_queries = [
        "What is machine learning?",
        "Tell me about Python programming",
        "Where is the Eiffel Tower?",
        "How do I cook pasta?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 50)
        
        results = db.query(query, n_results=3)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            continue
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]
        
        if documents:
            print("Top Results:")
            for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
                similarity = (1 / (1 + dist)) * 100
                print(f"\n  {i+1}. {meta.get('filename')} (Relevance: {similarity:.1f}%)")
                print(f"     Preview: {doc[:80]}...")
        else:
            print("❌ No results found")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)
    print("\nIf results match the queries, semantic search is working! ✓")

if __name__ == "__main__":
    test_semantic_search()