from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import string
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'

# Dữ liệu sản phẩm mẫu (dùng biến, không dùng database)
PRODUCTS = [
    {
        'id': 1,
        'icon': '🎮',
        'name': 'Auto Farm Pro',
        'description': 'Phần mềm tự động farm tài nguyên, exp và vật phẩm. Hỗ trợ đa game, an toàn 100%.',
        'price': 299000,
        'category': 'Auto Tool',
        'features': 'Auto farm|Multi-game support|Safe detection|24/7 running',
        'download_link': 'https://download.link/autofarm'
    },
    {
        'id': 2,
        'icon': '⚔️',
        'name': 'Combat Assistant',
        'description': 'Trợ lý chiến đấu thông minh, tự động combo skill và dodge. Tối ưu sát thương tối đa.',
        'price': 399000,
        'category': 'Combat Tool',
        'features': 'Smart combo|Auto dodge|Damage optimization|Skill rotation',
        'download_link': 'https://download.link/combat'
    },
    {
        'id': 3,
        'icon': '💰',
        'name': 'Trade Bot Elite',
        'description': 'Bot giao dịch tự động, phân tích thị trường và tối ưu lợi nhuận. Kiếm tiền 24/7.',
        'price': 599000,
        'category': 'Trading Bot',
        'features': 'Market analysis|Auto trading|Profit optimization|Risk management',
        'download_link': 'https://download.link/tradebot'
    },
    {
        'id': 4,
        'icon': '🔥',
        'name': 'Ultimate Package',
        'description': 'Gói combo tất cả phần mềm + cập nhật miễn phí + hỗ trợ 24/7. Giá ưu đãi nhất!',
        'price': 999000,
        'category': 'Bundle',
        'features': 'All tools included|Free updates|24/7 support|Premium features',
        'download_link': 'https://download.link/ultimate'
    }
]

def get_user():
    if 'user' not in session:
        session['user'] = {
            'username': 'admin',
            'email': 'admin@mail.com',
            'balance': 10000000,  # 10 triệu
            'purchases': []
        }
    return session['user']

@app.context_processor
def inject_user():
    user = session.get('user')
    return dict(current_user=user)

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/admin')
def admin_dashboard():
    user = get_user()
    if not user['username'] or user['username'] != 'admin':
        flash('Bạn không có quyền truy cập trang này!', 'error')
        return redirect(url_for('home'))
    # Giả lập danh sách thành viên (ở đây chỉ có admin, bạn có thể mở rộng)
    members = [session['user']]
    # Giả lập lịch sử giao dịch
    transactions = [
        {'username': 'admin', 'type': 'Nạp tiền', 'amount': 10000000, 'time': '2025-05-23 10:00'},
        # Thêm các giao dịch khác nếu muốn
    ]
    return render_template(
        'admin.html',
        user=user,
        members=members,
        transactions=transactions,
        products=PRODUCTS
    )

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    user = get_user()
    if not user['username'] or user['username'] != 'admin':
        flash('Bạn không có quyền truy cập trang này!', 'error')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        icon = request.form['icon']
        description = request.form['description']
        price = int(request.form['price'])
        category = request.form['category']
        features = request.form['features']
        download_link = request.form['download_link']
        new_id = max([p['id'] for p in PRODUCTS]) + 1 if PRODUCTS else 1
        PRODUCTS.append({
            'id': new_id,
            'icon': icon,
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'features': features,
            'download_link': download_link
        })
        flash('Thêm sản phẩm thành công!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_product.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = get_user()
        user['username'] = username
        user['email'] = f'{username}@mail.com'
        session['user'] = user
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return render_template('register.html')
        user = get_user()
        user['username'] = username
        user['email'] = email
        session['user'] = user
        flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    user = get_user()
    if not user['username']:
        return redirect(url_for('login'))
    purchases = user.get('purchases', [])
    purchases_info = []
    for p in purchases:
        prod = next((prod for prod in PRODUCTS if prod['id'] == p['product_id']), None)
        if prod:
            purchases_info.append({
                'id': p['id'],
                'product_id': prod['id'],
                'name': prod['name'],
                'icon': prod['icon'],
                'price': prod['price'],
                'download_count': p.get('download_count', 0),
                'purchase_date': p.get('purchase_date', '---'),
                'key': p.get('key', '---')
            })
    return render_template('profile.html', user=user, purchases=purchases_info)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((prod for prod in PRODUCTS if prod['id'] == product_id), None)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    return render_template('product_detail.html', product=product)

@app.route('/buy/<int:product_id>')
def buy_product(product_id):
    user = get_user()
    if not user['username']:
        flash('Vui lòng đăng nhập để mua hàng!', 'error')
        return redirect(url_for('login'))
    if any(p['product_id'] == product_id for p in user.get('purchases', [])):
        flash('Bạn đã sở hữu sản phẩm này!', 'warning')
        return redirect(url_for('profile'))
    product = next((prod for prod in PRODUCTS if prod['id'] == product_id), None)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    # Sinh key ngẫu nhiên
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    purchase = {
        'id': len(user['purchases']) + 1,
        'product_id': product_id,
        'download_count': 0,
        'purchase_date': 'Hôm nay',
        'key': key
    }
    user['purchases'].append(purchase)
    session['user'] = user
    flash(f'Mua {product["name"]} thành công! Check profile để download.', 'success')
    return redirect(url_for('profile'))

@app.route('/recharge', methods=['GET', 'POST'])
def recharge():
    user = get_user()
    if not user['username']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = int(request.form['amount'])
        user['balance'] += amount
        session['user'] = user
        flash(f'Nạp {amount:,} VNĐ thành công!', 'success')
        return redirect(url_for('profile'))
    return render_template('recharge.html')

@app.route('/download/<int:purchase_id>')
def download_product(purchase_id):
    user = get_user()
    if not user['username']:
        return redirect(url_for('login'))
    purchase = next((p for p in user.get('purchases', []) if p['id'] == purchase_id), None)
    if not purchase:
        flash('Không tìm thấy sản phẩm!', 'error')
        return redirect(url_for('profile'))
    product = next((prod for prod in PRODUCTS if prod['id'] == purchase['product_id']), None)
    if not product:
        flash('Không tìm thấy sản phẩm!', 'error')
        return redirect(url_for('profile'))
    purchase['download_count'] = purchase.get('download_count', 0) + 1
    session['user'] = user
    flash(f'Đang tải {product["name"]}... (Demo: {product["download_link"]})', 'info')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)