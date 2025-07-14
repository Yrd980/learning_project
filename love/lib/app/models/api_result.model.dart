import 'package:i_iwara/i18n/strings.g.dart' as slang;

class ApiResult<T> {
  final String message;
  final int code;
  final T? data;

  bool get isSuccess => code == 200;
  bool get isFail => !isSuccess;

  ApiResult._(this.message, this.data, this.code);

  factory ApiResult.success({
    String? message,
    T? data,
    int code = 200,
    String? custMessage,
  }) {
    return ApiResult._(
      custMessage ?? message ?? slang.t.common.success,
      data,
      code,
    );
  }

  factory ApiResult.fail(String message, {T? data, int code = 500}) {
    return ApiResult._(message, data, code);
  }

  @override
  String toString() {
    return 'ApiResult{message: $message, code: $code, data: $data, isSuccess: $isSuccess}';
  }
}

class AITestResult {
  final String? rawResponse;
  final String? translatedText;
  final bool connectionValid;
  final String custMessage;

  AITestResult({
    this.rawResponse,
    this.translatedText,
    this.connectionValid = false,
    required this.custMessage,
  });

  @override
  String toString() {
    return 'AITestResult{connectionValid: $connectionValid, custMessage: $custMessage, rawResponse: $rawResponse, translatedText: $translatedText}';
  }
}
