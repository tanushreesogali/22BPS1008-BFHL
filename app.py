from http.server import BaseHTTPRequestHandler
import json


def check_integer(value):
    """Helper function to check if a string is an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False


class handler(BaseHTTPRequestHandler):

    def _send_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            # Read request body
            length = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw_data)

            items = body.get("data", [])

            evens, odds, letters, specials = [], [], [], []
            alpha_chars, total_sum = [], 0

            for element in items:
                element_str = str(element)

                if check_integer(element_str):
                    num = int(element_str)
                    total_sum += num
                    (evens if num % 2 == 0 else odds).append(element_str)

                elif element_str.isalpha():
                    letters.append(element_str.upper())
                    alpha_chars.extend(list(element_str))

                else:
                    specials.append(element_str)

            # Build concatenated string
            alpha_chars.reverse()
            concat_string = "".join(
                char.upper() if idx % 2 == 0 else char.lower()
                for idx, char in enumerate(alpha_chars)
            )

            response_payload = {
                "is_success": True,
                "user_id": "tanushree_sogali",
                "email": "tanushree.sogali@gmail.com",
                "roll_number": "22BPS1008",
                "odd_numbers": odds,
                "even_numbers": evens,
                "alphabets": letters,
                "special_characters": specials,
                "sum": str(total_sum),
                "concat_string": concat_string,
            }

            self._send_headers(200)
            self.wfile.write(json.dumps(response_payload).encode("utf-8"))

        except Exception as err:
            error_payload = {"is_success": False, "error_message": str(err)}
            self._send_headers(400)
            self.wfile.write(json.dumps(error_payload).encode("utf-8"))
