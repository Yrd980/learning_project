import 'package:get/get.dart';
import 'package:i_iwara/app/models/api_result.model.dart';
import 'package:i_iwara/app/services/app_service.dart';
import 'package:i_iwara/app/ui/widgets/MDToastWidget.dart';
import 'package:i_iwara/i18n/strings.g.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:oktoast/oktoast.dart';

import '../../../../../common/constants.dart';
import '../../../../models/comment.model.dart';
import '../../../../services/comment_service.dart';

enum CommentType {
  post,
  video,
  profile,
  image;

  const CommentType();

  // 获取完整的API路径
  String getApiEndpoint(String id) => ApiConstants.comments(name, id);
}

class CommentController<T extends CommentType> extends GetxController {
  final String id;
  final T type;

  var comments = <Comment>[].obs;
  var isLoading = false.obs;
  var doneFirstTime = false.obs;
  var errorMessage = ''.obs;
  var currentPage = 0;
  final int pageSize = 20;
  var totalComments = 0.obs;
  var hasMore = true.obs;
  var pendingCount = 0.obs;

  // API 服务实例
  final CommentService _commentService = Get.find<CommentService>();

  CommentController({required this.id, required this.type});

  @override
  void onInit() {
    super.onInit();
    LogUtils.d('初始化', 'CommentController<${type.toString()}>');
    fetchComments(refresh: true);
  }
}
