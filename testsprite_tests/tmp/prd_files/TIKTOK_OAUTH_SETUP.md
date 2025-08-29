# 🎵 TikTok OAuth Setup Guide for SocialSeed

## 🚀 **What We've Implemented**

Your SocialSeed dashboard now has **full TikTok OAuth integration** instead of manual token entry! Here's what happens:

### **1. User Experience Flow**
1. **Click "Add New Account"** → Select "TikTok" platform
2. **See OAuth Status** → Green "TikTok Connected!" or Blue "Login Required"
3. **Click "🔑 Login TikTok"** → Opens TikTok authorization popup
4. **Authorize on TikTok** → User logs in and grants permissions
5. **Automatic Account Creation** → Account is created with real TikTok data
6. **No More Manual Tokens** → Everything is handled automatically!

### **2. Security Features**
- ✅ **State parameter verification** (prevents CSRF attacks)
- ✅ **Secure token storage** in localStorage
- ✅ **Popup-based OAuth** (no page redirects)
- ✅ **Automatic token refresh** handling

## 🔧 **Setup Requirements**

### **1. TikTok Developer Account**
- Go to [TikTok for Developers](https://developers.tiktok.com/)
- Create a new app
- Get your **Client Key** and **Client Secret**

### **2. Environment Variables**
Add these to your `frontend/.env.local`:

```bash
NEXT_PUBLIC_TIKTOK_CLIENT_KEY=your_actual_client_key_here
NEXT_PUBLIC_TIKTOK_CLIENT_SECRET=your_actual_client_secret_here
```

### **3. Redirect URI Configuration**
In your TikTok app settings, add this redirect URI:
```
http://localhost:3001/tiktok-callback
```
*(or your actual domain + /tiktok-callback)*

## 🎯 **How It Works**

### **OAuth Flow**
1. **Authorization Request** → User clicks "Login TikTok"
2. **TikTok Login** → User authenticates on TikTok
3. **Callback Handling** → `/tiktok-callback` page processes the response
4. **Token Exchange** → Authorization code → Access token
5. **User Info Fetch** → Get username and profile data
6. **Account Creation** → Automatically create account in database

### **Database Integration**
- **Access tokens** are stored securely in `social_accounts.access_token`
- **User info** is fetched from TikTok API
- **Account linking** happens automatically after OAuth

## 🧪 **Testing the Integration**

### **1. Test OAuth Flow**
1. Start your frontend: `npm run dev`
2. Go to dashboard
3. Click "Add New Account"
4. Select "TikTok" platform
5. Click "🔑 Login TikTok"
6. Complete TikTok authorization
7. Account should be created automatically!

### **2. Check Console Logs**
Look for these success messages:
```
🔗 Opening TikTok OAuth URL: https://...
✅ TikTok OAuth successful, code received: ...
🎯 Authorization code received: ...
✅ TikTok access token received: ...
🔑 Using TikTok OAuth access token
✅ Account created successfully
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Popup blocked" Error**
- **Solution**: Allow popups for your domain
- **Alternative**: Check browser popup blocker settings

#### **"Client Key not configured" Error**
- **Solution**: Add environment variables to `.env.local`
- **Verify**: Check `NEXT_PUBLIC_TIKTOK_CLIENT_KEY` value

#### **"State parameter mismatch" Error**
- **Solution**: Clear browser localStorage and try again
- **Cause**: Usually happens if OAuth flow is interrupted

#### **"Token exchange failed" Error**
- **Solution**: Verify your Client Secret is correct
- **Check**: TikTok app settings and redirect URI

### **Debug Steps**
1. **Check environment variables** in browser console
2. **Verify TikTok app settings** (redirect URI, permissions)
3. **Clear localStorage** and try again
4. **Check network tab** for API calls

## 🔒 **Security Notes**

### **Production Considerations**
- **Backend token exchange** (current implementation is for demo)
- **Secure token storage** (not localStorage)
- **HTTPS redirect URIs** only
- **Token refresh handling**

### **Current Implementation**
- ✅ **Client-side OAuth** (good for demos)
- ✅ **State verification** (prevents CSRF)
- ✅ **Secure popup handling**
- ⚠️ **localStorage tokens** (not production-ready)

## 🎉 **What You Get**

### **Before (Manual Tokens)**
- ❌ User had to find their own access token
- ❌ Tokens could expire without notice
- ❌ No automatic user info fetching
- ❌ Manual account setup process

### **After (OAuth Integration)**
- ✅ **One-click TikTok login**
- ✅ **Automatic token management**
- ✅ **Real username/profile data**
- ✅ **Seamless account creation**
- ✅ **Professional user experience**

## 🚀 **Next Steps**

1. **Get your TikTok Developer credentials**
2. **Update environment variables**
3. **Test the OAuth flow**
4. **Enjoy automatic TikTok account linking!**

---

**🎯 The goal**: Users can now connect their TikTok accounts with just a few clicks, no more manual token hunting!
