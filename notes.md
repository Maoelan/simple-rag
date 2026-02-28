# Notes

**English**

The design decision I made was to apply the Separation of Concerns principle by splitting the monolithic main.py into several layers, such as the API Layer (Router, Schemas), Business Logic Layer (RagWorkflow, RetrieveNode, AnswerNode), and Infrastructure Layer (DocumentStore and EmbeddingService). I also used explicit dependency injection to ensure each component is not tied to global variables, making the code easier to read and test in isolation.

One trade-off I considered was whether EmbeddingService should be injected into DocumentStore or directly into RetrieveNode. I decided to inject EmbeddingService into DocumentStore so that the storage logic is fully encapsulated, meaning RetrieveNode only needs to pass a query string to the search() method without knowing how vectors are generated. The downside is that DocumentStore now has two responsibilities: managing storage and generating embeddings. However, this is still beneficial because if the embedding model needs to be replaced in the future, changes only need to be made to EmbeddingService.

This refactored version improves maintainability because each layer can be modified, mocked (testing), or replaced without changing the others. For example, replacing the fake embedding with a real embedding model only requires changes to EmbeddingService, and replacing Qdrant with another vector store only requires changes to DocumentStore. The API behavior (/ask, /add, /status) remains the same, and the internal structure can now be tested in isolation.

---

**Bahasa Indonesia**

Keputusan desain yang saya ambil adalah menerapkan prinsip Separation of Concerns dengan memisahkan main.py yang monolik menjadi beberapa layer, seperti Layer API (Router, Schemas), Layer Business Logic (RagWorkflow, RetrieveNode, AnswerNode), dan Layer Infrastructure (DocumentStore dan EmbeddingService). Saya juga menggunakan dependency injection secara eksplisit agar setiap komponen tidak terikat pada variabel global sehingga kode lebih mudah dibaca dan diuji secara terisolasi.

Satu kompromi saya yaitu mempertimbangkan apakah EmbeddingService sebaiknya diinject ke DocumentStore atau lansung ke RetrieveNode. Saya memutuskan untuk menginject EmbeddingService ke DocumentStore agar logika penyimpanan sepenuhnya terenkapsulasi sehingga RetrieveNode cukup memberikan string query ke method search() tanpa perlu tahu bagaimana vector dihasilkan. Konsekuensinya, DocumentStore sekarang memiliki dua tanggung jawab yaitu mengelola penyimpanan dan menghasilkan embedding, akan tetapi ini tetap berguna karena jika kedepannya model embedding ingin diganti, perubahaan hanya perlu dilakukan pada Embedding Service saja.

Versi refactor ini meningkatkan kemudahan pemeliharaan karena setiap layer dapat dimodifikasi, dimock (testing), atau diganti tanpa mengubah layer lainnya. Misalnya mengganti fake embedding dengan model embedding yang nyata hanya membutuhkan perubahan pada EmbeddingService, dan mengganti Qdrant dengan vector store lainnya hanya perlu perubahan pada DocumentStore. Untuk perilaku API (/ask, /add, /status) tetap sama, dan struktur internal sekarang dapat diuji secara terisolasi.
