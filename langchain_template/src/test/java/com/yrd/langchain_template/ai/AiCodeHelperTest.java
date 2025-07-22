package com.yrd.langchain_template.ai;

import dev.langchain4j.data.message.ImageContent;
import dev.langchain4j.data.message.TextContent;
import dev.langchain4j.data.message.UserMessage;
import jakarta.annotation.Resource;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class AiCodeHelperTest {

    @Resource
    private AiCodeHelper aiCodeHelper;

    @Test
    void chat() {
        aiCodeHelper.chat("hello");
    }

    @Test
    void chatWithMessage() {
        UserMessage userMessage = UserMessage.from(
                TextContent.from("describe picture"),
                ImageContent.from("https://www.codefather.cn/logo.png")
        );
        aiCodeHelper.chatWithMessage(userMessage);
    }
}
