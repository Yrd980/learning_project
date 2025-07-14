import 'package:get/get.dart';
import 'package:i_iwara/app/models/api_result.model.dart';
import 'package:i_iwara/app/models/dto/user_dto.dart';
import 'package:i_iwara/app/models/history_record.dart';
import 'package:i_iwara/app/models/image.model.dart';
import 'package:i_iwara/app/repositories/history_repository.dart';
import 'package:i_iwara/app/services/gallery_service.dart';
import 'package:i_iwara/app/services/user_preference_service.dart';
import 'package:i_iwara/app/ui/widgets/MDToastWidget.dart';
import 'package:i_iwara/common/constants.dart';
import 'package:i_iwara/utils/logger_utils.dart';
import 'package:oktoast/oktoast.dart';

import '../../../../../common/enums/media_enums.dart';
import '../../../../models/user.model.dart';
import '../../video_detail/controllers/related_media_controller.dart';
class GalleryDetailController extends GetxController {
 
