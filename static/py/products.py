from supabase import create_client
import requests

class products:
    def __init__(self):
        self.base_url = "https://cgogqyorfzpxaiotscfp.supabase.co"
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnb2dxeW9yZnpweGFpb3RzY2ZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5ODMyMzcsImV4cCI6MjA2MzU1OTIzN30.enehR9wGHJf1xKO7d4XBbmjfdm80EvBKzaaPO3NPVAM'
        self.supabase = create_client(self.base_url, self.token)
        self.REPO = "voletrieulan0907/tool_changemail"

    def convert_github_url(self, url):
        if url.startswith('https://github.com/'):
            url = url.replace('https://github.com/', 'https://api.github.com/repos/', 1)
            if not url.endswith('/latest'):
                if not url.endswith('/'):
                    url += '/'
                url += 'latest'
        return url
    
    def check_update(self,url):
        # url = f"https://api.github.com/repos/{self.REPO}/releases/latest"
        urlnew = self.convert_github_url(url)
        try:
            response = requests.get(urlnew, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name']
                return latest_version
                # download_url = data['assets'][0]['browser_download_url'] if data['assets'] else None

                # if latest_version != CURRENT_VERSION:
                #     print(f"🔔 Có phiên bản mới: {latest_version}")
                #     if download_url:
                #         print(f"Tải tại: {download_url}")
                #     else:
                #         print("Không tìm thấy link tải.")
                # else:
                #     print("✅ Bạn đang dùng phiên bản mới nhất.")
            else:
                print(f"Lỗi khi kiểm tra phiên bản: {response.status_code}")
        except Exception as e:
            print(f"Lỗi kết nối: {e}")

    def get_products(self):
        res = self.supabase.table("PRODUCTS").select("*").execute()
        return res.data if res.data else []

    def get_next_id(self):
        products = self.get_products()
        if not products:
            return 1
        return max([p['id'] for p in products if 'id' in p and isinstance(p['id'], int)]) + 1

    def add_product(self, new_id, icon, name, price, description, category, features, download_link):
        version = self.check_update(download_link)
        try:
            self.supabase.table("PRODUCTS").insert({
                'id': new_id,
                'icon': icon,
                'name': name,
                'description': description,
                'price': price,
                'category': category,
                'features': features,
                'download_link': download_link,
                'version': version
            }).execute()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False