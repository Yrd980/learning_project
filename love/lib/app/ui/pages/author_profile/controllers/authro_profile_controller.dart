import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:i_iwara/app/ui/widgets/MDToastWidget.dart';
import 'package:i_iwara/i18n/strings.g.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:oktoast/oktoast.dart';

import '../../../../../common/constants.dart';
import '../../../../models/api_result.model.dart';
import '../../../../models/user.model.dart';
import '../../../../services/api_service.dart';
import '../../../../services/user_service.dart';
import '../../comment/controllers/comment_controller.dart';

class AuthorProfileController extends GetxController {
 
  final String username;
  final ApiService _apiService = Get.find();
  final UserService _userService = Get.find();
  late CommentController commentController;

  final RxBool isProfileLoading = RxBool(true);
  final Rxn<Widget> errorWidget = Rxn<Widget>();
  final Rxn<String> authorDescription = Rxn<String>();
  final Rxn<String> headerBackgroundUrl = Rxn<String>();
  final Rxn<User> author = Rxn<User>();
  final RxInt followingCounts = 0.obs;
  final RxInt followerCounts = 0.obs;
  final RxBool isDescriptionExpanded = false.obs;
  final Rxn<int> videoCounts = Rxn<int>();

  final RxBool isFriendRequestPending = false.obs;
  final RxBool isCommentSheetVisible = false.obs;
  Worker? worker;

  AuthorProfileController({required this.username});

  @override
  void onInit() {
    super.onInit();

    initFetch();

    worker = ever(_userService.currentUser, (user) {
      if (user != null) {
        fetchRelationshipStatus();
      }
    });
  }

  @override
  void onClose() {
    if (author.value != null) {
      Get.delete<CommentController>(tag: author.value!.id);
    }
    worker?.dispose();
    super.onClose();
  }

}
