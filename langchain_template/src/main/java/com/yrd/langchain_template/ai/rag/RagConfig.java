package com.yrd.langchain_template.ai.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.splitter.DocumentByParagraphSplitter;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.rag.content.retriever.ContentRetriever;
import dev.langchain4j.rag.content.retriever.EmbeddingStoreContentRetriever;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import jakarta.annotation.Resource;
import java.util.List;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RagConfig {

  @Resource private EmbeddingModel qwenEmbeddingModel;

  @Resource private EmbeddingStore<TextSegment> embeddingStore;

  @Bean
  public ContentRetriever contentRetriever() {

    List<Document> documents = FileSystemDocumentLoader.loadDocuments("src/main/resources/docs");

    DocumentByParagraphSplitter paragraphSplitter = new DocumentByParagraphSplitter(1000, 200);

    EmbeddingStoreIngestor ingestor =
        EmbeddingStoreIngestor.builder()
            .documentSplitter(paragraphSplitter)

            .textSegmentTransformer(
                textSegment ->
                    TextSegment.from(
                        textSegment.metadata().getString("file_name") + "\n" + textSegment.text(),
                        textSegment.metadata()))
      
            .embeddingModel(qwenEmbeddingModel)
            .embeddingStore(embeddingStore)
            .build();

    ingestor.ingest(documents);

    ContentRetriever contentRetriever =
        EmbeddingStoreContentRetriever.builder()
            .embeddingStore(embeddingStore)
            .embeddingModel(qwenEmbeddingModel)
            .maxResults(5) 
            .minScore(0.75) 
            .build();
    return contentRetriever;
  }
}
