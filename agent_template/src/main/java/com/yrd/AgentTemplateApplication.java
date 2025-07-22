package com.yrd;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class AgentTemplateApplication {

  public static void main(String[] args) {
    SpringApplication.run(AgentTemplateApplication.class, args);
  }
}
