import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class SchemaStorage {
  /// Loads the JSON schema from assets by filename
  Future<Map<String, dynamic>> loadSchema(String schemaFileName) async {
    final jsonString = await rootBundle.loadString('assets/schemas/$schemaFileName');
    return jsonDecode(jsonString) as Map<String, dynamic>;
  }
}
