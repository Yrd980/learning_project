import 'package:cached_network_image/cached_network_image.dart';
import 'package:extended_nested_scroll_view/extended_nested_scroll_view.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:i_iwara/app/models/api_result.model.dart';
import 'package:i_iwara/app/models/post.model.dart';
import 'package:i_iwara/app/routes/app_routes.dart';
import 'package:i_iwara/app/services/app_service.dart';
import 'package:i_iwara/app/services/post_service.dart';
import 'package:i_iwara/app/services/user_preference_service.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/author_profile_skeleton_widget.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/profile_image_model_tab_list_widget.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/profile_post_tab_list_widget.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/profile_video_tab_list_widget.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/profile_playlist_tab_list_widget.dart';
import 'package:i_iwara/app/ui/pages/comment/widgets/comment_input_dialog.dart';
import 'package:i_iwara/app/ui/pages/gallery_detail/widgets/horizontial_image_list.dart';
import 'package:i_iwara/app/ui/widgets/MDToastWidget.dart';
import 'package:i_iwara/app/ui/widgets/avatar_widget.dart';
import 'package:i_iwara/app/ui/widgets/top_padding_height_widget.dart';
import 'package:i_iwara/app/ui/widgets/user_name_widget.dart';
import 'package:i_iwara/utils/common_utils.dart';
import 'package:i_iwara/utils/image_utils.dart';
import 'package:oktoast/oktoast.dart';

import '../../../../common/constants.dart';
import '../../../services/user_service.dart';
import '../comment/widgets/comment_entry_area_widget.dart';
import '../comment/widgets/comment_section_widget.dart';
import '../popular_media_list/widgets/media_description_widget.dart';
import 'controllers/authro_profile_controller.dart';
import 'package:i_iwara/i18n/strings.g.dart' as slang;
import 'package:i_iwara/app/ui/widgets/follow_button_widget.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/post_input_dialog.dart';
import 'package:i_iwara/app/ui/pages/conversation/widgets/new_conversation_dialog.dart';
import 'package:i_iwara/app/ui/pages/author_profile/widgets/share_user_bottom_sheet.dart';
import 'package:i_iwara/app/ui/widgets/friend_button_widget.dart';

class AuthorProfilePage extends StatefulWidget {
  final String username;
  final String uniqueTag = DateTime.now().millisecondsSinceEpoch.toString();

  AuthorProfilePage({super.key, required this.username});

  @override
  _AuthorProfilePageState createState() => _AuthorProfilePageState();
}

class _AuthorProfilePageState extends State<AuthorProfilePage>
    with TickerProviderStateMixin {
  late final AuthorProfileController profileController;
  final UserService userService = Get.find<UserService>();
  final UserPreferenceService userPreferenceService =
      Get.find<UserPreferenceService>();
  late TabController primaryTC;
  late TabController videoSecondaryTC;
  late TabController imageSecondaryTC;
  late TabController playlistSecondaryTC;
  late String username;

  final GlobalKey<ExtendedNestedScrollViewState> _key =
      GlobalKey<ExtendedNestedScrollViewState>();
  late String uniqueTag;
  late ScrollController _tabBarScrollController;
  final GlobalKey<State<StatefulWidget>> _postListKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    uniqueTag = widget.uniqueTag;
    username = widget.username;
    profileController = Get.put(
      AuthorProfileController(username: username),
      tag: uniqueTag,
    );
    primaryTC = TabController(length: 4, vsync: this);
    videoSecondaryTC = TabController(length: 5, vsync: this);
    imageSecondaryTC = TabController(length: 5, vsync: this);
    playlistSecondaryTC = TabController(length: 5, vsync: this);
    _tabBarScrollController = ScrollController();
  }

  @override
  void dispose() {
    profileController.dispose();
    primaryTC.dispose();
    videoSecondaryTC.dispose();
    imageSecondaryTC.dispose();
    playlistSecondaryTC.dispose();
    _tabBarScrollController.dispose();
    Get.delete<AuthorProfileController>(tag: uniqueTag);
    super.dispose();
  }

  void _handleScroll(double delta) {
    if (_tabBarScrollController.hasClients) {
      final double newOffset = _tabBarScrollController.offset + delta;
      if (newOffset < 0) {
        _tabBarScrollController.jumpTo(0);
      } else if (newOffset > _tabBarScrollController.position.maxScrollExtent) {
        _tabBarScrollController.jumpTo(
          _tabBarScrollController.position.maxScrollExtent,
        );
      } else {
        _tabBarScrollController.jumpTo(newOffset);
      }
    }
  }
}
