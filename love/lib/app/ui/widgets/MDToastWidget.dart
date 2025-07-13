import 'package:flutter/material.dart';
import 'package:oktoast/oktoast.dart';

enum MDToastType { success, error, info, warning }

enum MDToastStyle { filled, outlined, light }

class MDToastWidget extends StatelessWidget {
  final String message;
  final MDToastType type;
  final MDToastWidget style;
  final Widget? leftIcon;
  final Widget? rightIcon;
  final TextStyle? textStyle;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final double? borderRadius;
  final double? elevation;
  final VoidCallback? onTap;
  final bool dismissible;

  const MDToastWidget({
    super.key,
    required this.message,
    this.type = MDToastType.info,
    this.style = MDToastStyle.filled,
    this.leftIcon,
    this.rightIcon,
    this.textStyle,
    this.padding,
    this.margin,
    this.borderRadius,
    this.elevation,
    this.onTap,
    this.dismissible = false,
  });
}
