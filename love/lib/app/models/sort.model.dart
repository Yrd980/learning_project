import 'package:flutter/material.dart';

import '../../common/constants.dart';

class Sort {
  final SortId id;
  final String label;
  final String extData;
  final StatelessWidget? icon;

  const Sort({
    required this.id,
    required this.label,
    this.icon,
    this.extData = '',
  });
}
