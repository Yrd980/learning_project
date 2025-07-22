package com.yrd.demo.invoke;

import jakarta.annotation.Resource;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.boot.CommandLineRunner;

// @Component
public class OllamaAiInvoke implements CommandLineRunner {

  @Resource private ChatModel ollamaChatModel;

  @Override
  public void run(String... args) throws Exception {
    AssistantMessage assistantMessage =
        ollamaChatModel.call(new Prompt("hi")).getResult().getOutput();
    System.out.println(assistantMessage.getText());
  }
}
