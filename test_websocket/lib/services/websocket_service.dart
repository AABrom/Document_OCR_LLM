import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketChannel? channel;

  Future<void> connect(String url) async {
    channel = WebSocketChannel.connect(Uri.parse(url));
  }

  bool get isConnected => channel != null;

  void sendMessage(String message) {
    if (channel == null) {
      throw Exception('WebSocket not connected');
    }
    channel!.sink.add(message);
  }

  void listen(
    void Function(dynamic) onData, {
    Function? onError,
    void Function()? onDone,
  }) {
    channel?.stream.listen(onData, onError: onError, onDone: onDone);
  }

  void close() {
    channel?.sink.close();
  }
}
