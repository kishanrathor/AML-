from  rag.vector_store import get_vector_store

def get_retriever():

    vectordb = get_vector_store()

    return vectordb.as_retriever(
        search_kwargs={"k": 3}
    )


def retrieve_context(query: str):

    retriever = get_retriever()

    docs = retriever.get_relevant_documents(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context