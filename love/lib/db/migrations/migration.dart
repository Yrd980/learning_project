import 'package:sqlite3/common.dart';

abstract class Migration {
  int get version;

  String get description;

  void up(CommonDatabase db);

  void down(CommonDatabase db);
}
