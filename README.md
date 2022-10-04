[This is a work in progress]

App url: https://anukriti-ranjan-in-patent-search-streamlit-app-drhhdz.streamlitapp.com/

### Searching titles of patents filed by Indians in India

The current patent search interface provided by Indian Patent Advanced Search System (developed by Indian patent office) relies on lexical search for searching patents. With the prior art an essential point of study and search before filing patents, this kind of search prevents discovery of previous work.The filing of patents has been increasing in recents years and applicants need a better search interface for the review of the existing work.

![out](https://user-images.githubusercontent.com/89630232/193036815-b0a271ee-a920-4fe5-9eb2-b620745b3b61.png)

### Methodology

For the purpose of developing a search interface, ~180K patent titles have been scraped from [Indian Patent Advanced Search System](https://ipindiaservices.gov.in/publicsearch/) across ~7200 pages. (This model will be perfected on both abstracts and titles in the coming days).

The app lets the user compare search results from 2 search types:
1) BM25 - which is a bag-of-words retrieval method that depends on exact matching of terms (currently not implemented in the URL)

2) Semantic similarity search which searches the vector space of the documents for close matches. In this case, the search is able to retrieve synonyms and similar meanings. Currently, a lean model of sbert (~130 MB) is used for the purpose of encoding documents and approximate nearest neighbour is applied for retrieving search results.



References:

https://ai.googleblog.com/2022/08/announcing-patent-phrase-similarity.html?m=1

