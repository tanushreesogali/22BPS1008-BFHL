from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

def check_if_integer(value_str):
    try:
        int(value_str)
        return True
    except ValueError:
        return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length_val = int(self.headers['Content-Length'])
            post_data_content = self.rfile.read(content_length_val)
            parsed_data = json.loads(post_data_content.decode('utf-8'))
            
            input_values = parsed_data.get('data', [])
            
            even_values = []
            odd_values = []
            letter_chars = []
            special_chars = []
            total_sum = 0
            alpha_characters = []
            
            for element in input_values:
                element_str = str(element)
                
                if check_if_integer(element_str):
                    num_value = int(element_str)
                    total_sum += num_value
                    
                    if num_value % 2 == 0:
                        even_values.append(element_str)
                    else:
                        odd_values.append(element_str)
                elif element_str.isalpha():
                    letter_chars.append(element_str.upper())
                    for character in element_str:
                        alpha_characters.append(character)
                else:
                    special_chars.append(element_str)
            
            concatenated_result = ""
            alpha_characters.reverse()
            
            for index, character in enumerate(alpha_characters):
                if index % 2 == 0:
                    concatenated_result += character.upper()
                else:
                    concatenated_result += character.lower()
            
            response_data = {
                "is_success": True,
                "user_id": "tanushree_sogali",
                "email": "tanushree.sogali@gmail.com",
                "roll_number": "22BPS1008",
                "odd_numbers": odd_values,
                "even_numbers": even_values,
                "alphabets": letter_chars,
                "special_characters": special_chars,
                "sum": str(total_sum),
                "concat_string": concatenated_result
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as error:
            error_response_data = {
                "is_success": False,
                "error_message": str(error)
            }
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response_data).encode('utf-8'))
