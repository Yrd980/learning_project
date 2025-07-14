import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:i_iwara/app/models/message_and_conversation.model.dart';
import 'package:i_iwara/app/models/post.model.dart';
import 'package:i_iwara/app/ui/pages/conversation/conversation_page.dart';
import 'package:i_iwara/app/ui/pages/conversation/widgets/message_list_widget.dart';
import 'package:i_iwara/app/ui/pages/favorite/favorite_folder_detail_page.dart';
import 'package:i_iwara/app/ui/pages/favorite/favorite_list_page.dart';
import 'package:i_iwara/app/ui/pages/favorites/my_favorites.dart';
import 'package:i_iwara/app/ui/pages/follows/follows_page.dart';
import 'package:i_iwara/app/ui/pages/forum/thread_detail_page.dart';
import 'package:i_iwara/app/ui/pages/forum/thread_list_page.dart';
import 'package:i_iwara/app/ui/pages/friends/friends_page.dart';
import 'package:i_iwara/app/ui/pages/gallery_detail/widgets/horizontial_image_list.dart';
import 'package:i_iwara/app/ui/pages/gallery_detail/widgets/my_gallery_photo_view_wrapper.dart';
import 'package:i_iwara/app/ui/pages/history/history_list_page.dart';
import 'package:i_iwara/app/ui/pages/notifications/notification_list_page.dart';
import 'package:i_iwara/app/ui/pages/play_list/play_list.dart';
import 'package:i_iwara/app/ui/pages/play_list/play_list_detail.dart';
import 'package:i_iwara/app/ui/pages/tag_blacklist/tag_blacklist_page.dart';
import 'package:i_iwara/app/ui/pages/video_detail/controllers/my_video_state_controller.dart';
import 'package:i_iwara/app/ui/pages/video_detail/video_detail_page_v2.dart';
import 'package:i_iwara/app/ui/pages/video_detail/widgets/player/my_video_screen.dart';
import 'package:i_iwara/app/ui/pages/download/download_task_list_page.dart';
import 'package:i_iwara/app/ui/pages/download/gallery_download_task_detail_page.dart';

import '../routes/app_routes.dart';
import '../ui/pages/author_profile/author_profile_page.dart';
import '../ui/pages/gallery_detail/gallery_detail_page.dart';
import '../ui/pages/search/search_result.dart';
import '../ui/pages/post_detail/post_detail_page.dart';

enum TransitionType { slideRight, fade, none }

class AppService extends GetxService {
  static const double titleBarHeight = 26.0;

  final RxBool _showTitleBar = false.obs;

  final RxBool _showRailNavi = true.obs;
  final RxBool _showBottomNavi = true.obs;
  final RxInt _currentIndex = 0.obs;

  static final GlobalKey<ScaffoldState> globalDrawerKey =
      GlobalKey<ScaffoldState>();

  static final GlobalKey<NavigatorState> homeNavigatorKey = Get.nestedKey(
    Routes.HOME,
  )!.navigatorKey;

  AppService() {
    if (GetPlatform.isDesktop && !GetPlatform.isWeb) {
      _showTitleBar.value = true;
    }
  }

  bool get showTitleBar => _showTitleBar.value;

  set showTitleBar(bool value) => {
    if (GetPlatform.isDesktop && !GetPlatform.isWeb)
      {_showTitleBar.value = value},
  };

  bool get showRailNavi => _showRailNavi.value;

  set showBottomNavi(bool value) => _showBottomNavi.value = value;

  bool get showBottomNavi => _showBottomNavi.value;

  set showRailNavi(bool value) => _showRailNavi.value = value;

  int get currentIndex => _currentIndex.value;

  set currentIndex(int value) => _currentIndex.value = value;

  static void switchGlobalDrawer() {
    if (globalDrawerKey.currentState!.isDrawerOpen) {
      globalDrawerKey.currentState!.openEndDrawer();
    } else {
      globalDrawerKey.currentState!.openDrawer();
    }
  }

  static void hideGlobalDrawer() {
    globalDrawerKey.currentState!.closeDrawer();
  }

  void toggleTitleBar() {
    _showTitleBar.value = !_showTitleBar.value;
  }

  updateIndex(int value) {
    _currentIndex.value = value;
  }

  static void tryPop({bool closeAll = false}) {
    if (AppService.globalDrawerKey.currentState!.isDrawerOpen) {
      AppService.globalDrawerKey.currentState!.openEndDrawer();
    } else {
      if (Get.isDialogOpen ?? false) {
        Get.close(closeAll: closeAll);
      } else if (Get.isBottomSheetOpen ?? false) {
        Get.close(closeAll: closeAll);
      } else {
        GetDelegate? homeDele = Get.nestedKey(Routes.HOME);
        GetDelegate? rootDele = Get.nestedKey(null);

        if (homeDele?.canBack ?? false) {
          homeDele?.back();
        } else if (homeDele?.navigatorKey.currentState?.canPop() ?? false) {
          homeDele?.navigatorKey.currentState?.pop();
        } else if (rootDele?.canBack ?? false) {
          rootDele?.back();
        } else {
          SystemNavigator.pop();
        }
      }
    }
  }

  void hideSystemUI({hideTitleBar = true, hideRailNavi = true}) {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    showTitleBar = !hideTitleBar;
    showRailNavi = !hideRailNavi;
  }

  void showSystemUI() {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    showTitleBar = true;
    showRailNavi = true;
  }
}

class NaviService {
  static void _navigateToPage({
    required String routeName,
    required Widget page,
    Duration transitionDuration = const Duration(milliseconds: 200),
    TransitionType transitionType = TransitionType.slideRight,
  }) {
    AppService.homeNavigatorKey.currentState?.push(
      PageRouteBuilder(
        settings: RouteSettings(name: routeName),
        pageBuilder: (context, animation, secondaryAnimation) {
          return page;
        },
        transitionDuration: transitionDuration,
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          switch (transitionType) {
            case TransitionType.slideRight:
              return SlideTransition(
                position: Tween<Offset>(
                  begin: const Offset(1, 0),
                  end: Offset.zero,
                ).animate(animation),
                child: child,
              );
            case TransitionType.fade:
              return FadeTransition(opacity: animation, child: child);
            case TransitionType.none:
              return child;
          }
        },
      ),
    );
  }

  static void navigateToAuthorProfilePage(String username) {
    _navigateToPage(
      routeName: Routes.AUTHOR_PROFILE(username),
      page: AuthorProfilePage(username: username),
    );
  }

  static void navigateToGalleryDetailPage(String id) {
    _navigateToPage(routeName: Routes.GALLERY_DETAIL(id), page: )
  }
}
