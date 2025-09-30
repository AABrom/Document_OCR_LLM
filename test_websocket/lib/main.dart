import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'schema_repository/schema_storage.dart';
import 'services/websocket_service.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final SchemaStorage _schemaStorage = SchemaStorage();
  final WebSocketService _webSocketService = WebSocketService();

  final ImagePicker _picker = ImagePicker();

  String _selectedAnalysisType = 'blood_test';
  Map<String, dynamic>? _loadedSchema;
  String _serverResponse = '';

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
    _loadSchema(_selectedAnalysisType);
  }

  Future<void> _connectWebSocket() async {
    try {
      await _webSocketService.connect('ws://localhost:8080/ws');
      _webSocketService.listen(
        (data) {
          setState(() {
            _serverResponse = data.toString();
          });
        },
        onError: (error) => print('WebSocket error: $error'),
        onDone: () => print('WebSocket closed'),
      );
    } catch (e) {
      print('Error connecting WebSocket: $e');
    }
  }

  Future<void> _loadSchema(String name) async {
    final schemaFile = '$name.json';
    final schema = await _schemaStorage.loadSchema(schemaFile);
    setState(() {
      _loadedSchema = schema;
      _serverResponse = '';
    });
  }

  void _onAnalysisTypeChanged(String newType) async {
    setState(() {
      _selectedAnalysisType = newType;
    });
    await _loadSchema(newType);
  }

  Future<void> _pickAndSendImageWithSchema() async {
    final XFile? imageFile = await _picker.pickImage(
      source: ImageSource.gallery,
    );
    if (imageFile == null) {
      print('No image selected.');
      return;
    }

    final bytes = await imageFile.readAsBytes();
    final base64Image = base64Encode(bytes);

    if (!_webSocketService.isConnected) {
      print('WebSocket is not connected');
      return;
    }

    if (_loadedSchema == null) {
      print('Schema not loaded');
      return;
    }

    final message = jsonEncode({
      'image_data': base64Image,
      'schema': _loadedSchema,
    });

    _webSocketService.channel?.sink.add(message);
    print('Image and schema sent to server');
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Schema & WebSocket Demo',
      home: Scaffold(
        appBar: AppBar(title: Text('Schema & WebSocket Demo')),
        body: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            children: [
              DropdownButton<String>(
                value: _selectedAnalysisType,
                items: [
                  DropdownMenuItem(
                    value: 'blood_test',
                    child: Text('Blood Test'),
                  ),
                ],
                onChanged: (value) {
                  if (value != null) _onAnalysisTypeChanged(value);
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _pickAndSendImageWithSchema,
                child: Text('Upload Image + Send with Schema'),
              ),
              SizedBox(height: 20),
              Expanded(
                child: SingleChildScrollView(child: Text(_serverResponse)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
