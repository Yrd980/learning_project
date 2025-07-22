package com.yrd.demo.invoke;

import cn.hutool.http.HttpRequest;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;

public class HttpAiInvoke {

  public static void main(String[] args) {

    String apiKey = TestApiKey.API_KEY;

    String url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";

    JSONObject messagesJson = new JSONObject();

    JSONObject systemMessage = new JSONObject();
    systemMessage.set("role", "system");
    systemMessage.set("content", "You are a helpful assistant.");

    JSONObject userMessage = new JSONObject();
    userMessage.set("role", "user");
    userMessage.set("content", "who are you？");

    messagesJson.set("messages", JSONUtil.createArray().set(systemMessage).set(userMessage));

    JSONObject parametersJson = new JSONObject();
    parametersJson.set("result_format", "message");

    JSONObject requestJson = new JSONObject();
    requestJson.set("model", "qwen-plus");
    requestJson.set("input", messagesJson);
    requestJson.set("parameters", parametersJson);

    String result =
        HttpRequest.post(url)
            .header("Authorization", "Bearer " + apiKey)
            .header("Content-Type", "application/json")
            .body(requestJson.toString())
            .execute()
            .body();

    System.out.println(result);
  }
}
