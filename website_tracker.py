    listings = soup.find_all('div', class_='_1AtVbE')

    print(f"🔍 Found {len(listings)} listings...")

    for index, item in enumerate(listings):
        print(f"\n--- Product Block #{index+1} ---")

        title_tag = item.find('div', class_='_4rR01T') or item.find('a', class_='IRpwTa')
        price_tag = item.find('div', class_='_30jeq3 _1_WHN1') or item.find('div', class_='_30jeq3')
        link_tag = item.find('a', href=True)

        print("Title:", title_tag.text.strip() if title_tag else "Not found")
        print("Price:", price_tag.text.strip() if price_tag else "Not found")
        print("Link:", ("https://www.flipkart.com" + link_tag['href'].split('?')[0]) if link_tag else "Not found")

        if title_tag and price_tag and link_tag:
            products.append({
                'Title': title_tag.text.strip(),
                'Price': price_tag.text.strip(),
                'Link': "https://www.flipkart.com" + link_tag['href'].split('?')[0]
            })

        if len(products) == 5:
            break
