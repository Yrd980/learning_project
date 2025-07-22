package com.yrd.langchain_template.ai;

import com.yrd.langchain_template.ai.tools.InterviewQuestionTool;
import dev.langchain4j.mcp.McpToolProvider;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.chat.StreamingChatModel;
import dev.langchain4j.rag.content.retriever.ContentRetriever;
import dev.langchain4j.service.AiServices;
import jakarta.annotation.Resource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AiCodeHelperServiceFactory {

  @Resource private ChatModel myQwenChatModel;

  @Resource private StreamingChatModel qwenStreamingChatModel;

  @Resource private ContentRetriever contentRetriever;

  @Resource private McpToolProvider mcpToolProvider;

  @Bean
  public AiCodeHelperService aiCodeHelperService() {

    ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);
    AiCodeHelperService aiCodeHelperService =
        AiServices.builder(AiCodeHelperService.class)
            .chatModel(myQwenChatModel)
            .streamingChatModel(qwenStreamingChatModel)
            .chatMemory(chatMemory)
            .chatMemoryProvider(memoryId -> MessageWindowChatMemory.withMaxMessages(10)) 
            .contentRetriever(contentRetriever) 
            .tools(new InterviewQuestionTool()) 
            .toolProvider(mcpToolProvider) 
            .build();
    return aiCodeHelperService;
  }
}
