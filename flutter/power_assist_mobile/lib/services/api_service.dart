import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({required this.baseUrl});

  Future<Map<String, dynamic>> uploadDocument(String filePath) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/v1/upload'),
    );
    
    request.files.add(await http.MultipartFile.fromPath('file', filePath));
    
    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    
    if (response.statusCode == 200) {
      return json.decode(responseData);
    } else {
      throw Exception('Failed to upload document');
    }
  }

  Future<List<Map<String, dynamic>>> getDocuments() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/v1/documents'),
    );

    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(json.decode(response.body));
    } else {
      throw Exception('Failed to load documents');
    }
  }

  Future<Map<String, dynamic>> getDocument(String documentId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/v1/documents/$documentId'),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load document');
    }
  }
}
