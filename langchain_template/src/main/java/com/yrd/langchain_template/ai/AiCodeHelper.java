package com.yrd.langchain_template.ai;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.chat.response.ChatResponse;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class AiCodeHelper {

  @Resource private ChatModel qwenChatModel;

  private static final String SYSTEM_MESSAGE =
"""
           Role: You are a Programming Assistant specializing in helping users with coding education and career development. Focus on these 4 key areas:

            1.Structured Learning Paths – Provide clear, step-by-step roadmaps for mastering programming languages/frameworks (e.g., Python, Web Dev, Data Science).

            2.Project Guidance – Suggest hands-on projects tailored to skill levels (beginner to advanced), with tips on design, implementation, and portfolio presentation.

            3.Job Search Strategy – Offer end-to-end career advice: resume/CV optimization, LinkedIn/profile tips, job application tactics, and negotiation techniques.

            4.Interview Prep – Share high-frequency coding interview questions (LeetCode-style, system design), behavioral tips (STAR method), and mock interview feedback.\
""";

  public String chat(String message) {
    SystemMessage systemMessage = SystemMessage.from(SYSTEM_MESSAGE);
    UserMessage userMessage = UserMessage.from(message);
    ChatResponse chatResponse = qwenChatModel.chat(systemMessage, userMessage);
    AiMessage aiMessage = chatResponse.aiMessage();
    log.info(aiMessage.toString());
    return aiMessage.text();
  }

  public String chatWithMessage(UserMessage userMessage) {
    ChatResponse chatResponse = qwenChatModel.chat(userMessage);
    AiMessage aiMessage = chatResponse.aiMessage();
    log.info(aiMessage.toString());
    return aiMessage.text();
  }
}
