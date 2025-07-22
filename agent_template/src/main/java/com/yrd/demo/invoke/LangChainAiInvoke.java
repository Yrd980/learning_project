package com.yrd.demo.invoke;

import dev.langchain4j.community.model.dashscope.QwenChatModel;
import dev.langchain4j.model.chat.ChatLanguageModel;

public class LangChainAiInvoke {

  public static void main(String[] args) {
    ChatLanguageModel qwenChatModel =
        QwenChatModel.builder().apiKey(TestApiKey.API_KEY).modelName("qwen-max").build();
    String answer = qwenChatModel.chat("this is ai agent template");
    System.out.println(answer);
  }
}
