import requests
import time

# Fungsi untuk mendapatkan semua pasangan kripto di Indodax
def get_all_pairs():
    api_url = 'https://indodax.com/api/pairs'
    response = requests.get(api_url)
    data = response.json()
    return [pair['symbol'] for pair in data]

# Fungsi untuk mendapatkan harga kripto
def get_crypto_price(pair):
    api_url = f'https://indodax.com/api/ticker/{pair.lower()}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        last_price = float(data.get('ticker', {}).get('last', 0))
        return last_price
    else:
        return None

# Fungsi untuk memonitor kenaikan harga di atas 5%
def monitor_price_increase(threshold_percent=5):
    all_pairs = get_all_pairs()

    # Inisialisasi harga awal untuk setiap pasangan
    initial_prices = {pair: get_crypto_price(pair) for pair in all_pairs}

    while True:
        for pair in all_pairs:
            current_price = get_crypto_price(pair)

            if current_price is not None:
                initial_price = initial_prices.get(pair, current_price)
                
                # Memastikan initial_price tidak sama dengan 0
                if initial_price != 0:
                    percentage_increase = ((current_price - initial_price) / initial_price) * 100
                    if percentage_increase > threshold_percent:
                        print(f"{pair.upper()}: Harga naik \033[92m{percentage_increase:.2f}%\033[0m")

        time.sleep(15)  # Periksa setiap 15 detik

if __name__ == '__main__':
    monitor_price_increase()
