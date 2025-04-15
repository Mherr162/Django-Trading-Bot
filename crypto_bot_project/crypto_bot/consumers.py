import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import logs, default_timezone
import re
import datetime
import pytz

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', '')
        
        if message_type == 'get_logs':
            # Get timezone from request or use default
            timezone = text_data_json.get('timezone', default_timezone)
            
            # Send current logs with color coding
            formatted_logs = []
            
            for log in logs:
                # Determine log class based on level
                if '[ERROR]' in log:
                    log_class = 'error'
                elif '[SUCCESS]' in log:
                    log_class = 'success'
                elif '[WARNING]' in log:
                    log_class = 'warning'
                else:
                    log_class = 'info'
                
                # Convert timestamp to the requested timezone if needed
                log_text = log
                if timezone != default_timezone:
                    # Extract timestamp from log
                    timestamp_match = re.match(r'\[(.*?)\]', log)
                    if timestamp_match:
                        timestamp_str = timestamp_match.group(1)
                        try:
                            # Parse the timestamp
                            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                            # Assume the timestamp is in the default timezone
                            source_tz = pytz.timezone(default_timezone)
                            target_tz = pytz.timezone(timezone)
                            # Make the timestamp timezone-aware
                            timestamp = source_tz.localize(timestamp)
                            # Convert to target timezone
                            converted_timestamp = timestamp.astimezone(target_tz)
                            # Format the new timestamp
                            new_timestamp_str = converted_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                            # Replace the timestamp in the log
                            log_text = log.replace(f'[{timestamp_str}]', f'[{new_timestamp_str}]')
                        except Exception as e:
                            # If conversion fails, use the original log
                            pass
                
                formatted_logs.append({
                    'text': log_text,
                    'class': log_class
                })
            
            await self.send(text_data=json.dumps({
                'type': 'log_update',
                'logs': formatted_logs
            }))
        elif message_type == 'clear_logs':
            # Clear logs logic can be implemented here if needed
            pass 