import 'package:get/get.dart';
import 'package:i_iwara/app/models/api_result.model.dart';
import 'package:i_iwara/app/models/comment.model.dart';
import 'package:i_iwara/app/models/page_data.model.dart';
import 'package:i_iwara/app/models/rules.model.dart';
import 'package:i_iwara/app/services/api_service.dart';
import 'package:i_iwara/common/constants.dart';
import 'package:i_iwara/i18n/strings.g.dart';
import 'package:i_iwara/utils/logger_utils.dart';

class CommentService extends GetxService {
  final ApiService _apiService = Get.find<ApiService>();

  Future<ApiResult<PageData<Comment>>> getComments({
    required String type,
    required String id,
    String? parentId,
    int page = 0,
    int limit = 20,
  }) async {
    try {
      final response = await _apiService.get(
        ApiConstants.comments(type, id),
        queryParameters: {
          'page': page,
          'limit': limit,
          if (parentId != null) 'parent': parentId,
        },
      );

      final PageData<Comment> pageData = PageData.fromJsonWithConverter(
        response.data,
        Comment.fromJson,
      );

      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get comment fail', tag: 'CommentService', error: e);
      return ApiResult.fail(t.errors.failedToFetchComments);
    }
  }

  Future<ApiResult<void>> deleteComment(String id) async {
    try {
      await _apiService.delete(ApiConstants.comment(id));
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('delete comment fail', tag: 'CommentService', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult<void>> editComment(String id, String body) async {
    try {
      await _apiService.put(ApiConstants.comment(id), data: {'body': body});
      return ApiResult.success();
    } catch (e) {
      LogUtils.e('edit comment fail', tag: 'CommentService', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult<Comment>> postComment({
    required String type,
    required String id,
    required String body,
    String? parentId,
  }) async {
    try {
      final response = await _apiService.post(
        ApiConstants.comments(type, id),
        data: {
          'body': body,
          'rulesAgreement': true,
          if (parentId != null) 'parentId': parentId,
        },
      );

      return ApiResult.success(data: Comment.fromJson(response.data));
    } catch (e) {
      LogUtils.e('post comment fail', tag: 'CommentService', error: e);
      return ApiResult.fail(t.errors.failedToOperate);
    }
  }

  Future<ApiResult<PageData<RulesModel>>> getRules() async {
    try {
      final response = await _apiService.get(ApiConstants.rules);
      final List<RulesModel> results = (response.data['results'] as List)
          .map((rule) {
            if (rule['body'] is! Map) {
              LogUtils.e(
                'rule body field formate error: ${rule['body']}',
                tag: 'CommentService',
              );
              return null;
            }
            try {
              return RulesModel.fromJson(rule);
            } catch (e) {
              LogUtils.e('parse rule error', tag: 'CommentService', error: e);
              return null;
            }
          })
          .where((rule) => rule != null)
          .cast<RulesModel>()
          .toList();

      final PageData<RulesModel> pageData = PageData(
        page: response.data['page'],
        limit: response.data['limit'],
        count: response.data['count'],
        results: results,
      );
      return ApiResult.success(data: pageData);
    } catch (e) {
      LogUtils.e('get rule fail', tag: 'CommentService', error: e);
      return ApiResult.fail(t.errors.failedToFetchData);
    }
  }
}
