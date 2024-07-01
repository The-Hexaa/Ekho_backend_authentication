from app import create_app
import ssl

app = create_app()

if __name__ == '__main__':
    # SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        
    ssl_context.load_cert_chain('keys/cert.pem', 'keys/key.pem')

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
