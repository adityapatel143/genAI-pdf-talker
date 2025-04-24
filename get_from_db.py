from embedder_and_retriver import retriver

def retrive_data(data):
    # search_result = retriver.similarity_search(
    #     data,
    #     k=2
    # )
    # return search_result

    res = retriver.as_retriever(search_type="mmr", search_kwargs={"k": 1})
    return  res.invoke(data)

# print(search_result)

if __name__ == "__main__":
    retrive_data()