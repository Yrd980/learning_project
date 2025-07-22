package com.yrd.langchain_template.ai;

import com.yrd.langchain_template.ai.guardrail.SafeInputGuardrail;
import dev.langchain4j.service.*;
import dev.langchain4j.service.guardrail.InputGuardrails;
import java.util.List;
import reactor.core.publisher.Flux;

@InputGuardrails({SafeInputGuardrail.class})
public interface AiCodeHelperService {

  @SystemMessage(fromResource = "system-prompt.txt")
  String chat(String userMessage);

  @SystemMessage(fromResource = "system-prompt.txt")
  Report chatForReport(String userMessage);

  record Report(String name, List<String> suggestionList) {}

  @SystemMessage(fromResource = "system-prompt.txt")
  Result<String> chatWithRag(String userMessage);

  Flux<String> chatStream(@MemoryId int memoryId, @UserMessage String userMessage);
}
