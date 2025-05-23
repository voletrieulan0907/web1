from supabase import create_client

class products:
    def __init__(self):
        self.base_url = "https://cgogqyorfzpxaiotscfp.supabase.co"
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnb2dxeW9yZnpweGFpb3RzY2ZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5ODMyMzcsImV4cCI6MjA2MzU1OTIzN30.enehR9wGHJf1xKO7d4XBbmjfdm80EvBKzaaPO3NPVAM'
        self.supabase = create_client(self.base_url, self.token)

    def get_products(self):
        res = self.supabase.table("PRODUCTS").select("*").execute()
        return res.data if res.data else []

    def get_next_id(self):
        products = self.get_products()
        if not products:
            return 1
        return max([p['id'] for p in products if 'id' in p and isinstance(p['id'], int)]) + 1

    def add_product(self, new_id, icon, name, price, description, category, features, download_link):
        try:
            self.supabase.table("PRODUCTS").insert({
                'id': new_id,
                'icon': icon,
                'name': name,
                'description': description,
                'price': price,
                'category': category,
                'features': features,
                'download_link': download_link
            }).execute()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False