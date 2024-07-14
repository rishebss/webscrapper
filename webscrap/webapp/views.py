from django.shortcuts import render,HttpResponse
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import json
import random

def home(request):
    return render(request, "home.html")

def scrapall(request):
    url = request.GET.get('url')
    content = ""
    links = []
    media = []
    metadata = {}
    prices = []

    if url:
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, "html.parser")
            
            # Extract text content
            content = soup.get_text()

            # Extract all links
            for link in soup.find_all('a'):
                links.append(link.get('href'))

            # Extract media (images, videos, etc.)
            for img in soup.find_all('img'):
                media.append(img.get('src'))

            # Extract metadata (title, description, author, etc.)
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text()

            meta_tags = soup.find_all('meta')
            for meta_tag in meta_tags:
                if 'name' in meta_tag.attrs and 'content' in meta_tag.attrs:
                    metadata[meta_tag['name'].lower()] = meta_tag['content']
                elif 'property' in meta_tag.attrs and 'content' in meta_tag.attrs:
                    metadata[meta_tag['property'].lower()] = meta_tag['content']

            script_tags = soup.find_all('script', type='application/ld+json')
            for script_tag in script_tags:
                try:
                    json_data = json.loads(script_tag.string)
                    if isinstance(json_data, dict):
                        for key, value in json_data.items():
                            metadata[key.lower()] = value
                except json.JSONDecodeError as e:
                    pass  # Handle JSON decoding errors if needed 

            for price_div in soup.find_all('div', class_='a-section'):
                price_text = price_div.get_text(strip=True)
                # Add logic to check if the text is a price (e.g., contains a currency symbol)
                if any(char.isdigit() for char in price_text):
                    prices.append(price_text)           
            
                 
        except Exception as e:
            content = f"An error occurred: {e}"

    return render(request, "scrapall.html", {"content": content, "links": links, "media": media, "metadata": metadata})