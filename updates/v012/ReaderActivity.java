package com.openai.cod15guide;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceError;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
/** Displays the publisher's complete live page, without a JavaScript bridge. */
public class ReaderActivity extends Activity {
 private WebView page;private String currentUrl;
 static boolean trusted(Uri uri){if(uri==null||!"https".equalsIgnoreCase(uri.getScheme()))return false;String h=uri.getHost();return "www.codzombiesguides.com".equalsIgnoreCase(h)||"codzombiesguides.com".equalsIgnoreCase(h)||"codzombified.blogspot.com".equalsIgnoreCase(h);}
 @Override protected void onCreate(Bundle state){super.onCreate(state);Uri uri=getIntent().getData();if(!trusted(uri)){finish();return;}currentUrl=uri.toString();
  LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(Color.rgb(16,19,24));root.setOnApplyWindowInsetsListener((v,i)->{v.setPadding(i.getSystemWindowInsetLeft(),i.getSystemWindowInsetTop(),i.getSystemWindowInsetRight(),i.getSystemWindowInsetBottom());return i.consumeSystemWindowInsets();});
  LinearLayout bar=new LinearLayout(this);Button back=new Button(this);back.setText("返回教程");back.setOnClickListener(v->finish());Button browser=new Button(this);browser.setText("浏览器打开");browser.setOnClickListener(v->openExternal(Uri.parse(currentUrl)));Button refresh=new Button(this);refresh.setText("刷新");refresh.setOnClickListener(v->page.reload());bar.addView(back,new LinearLayout.LayoutParams(0,-2,1));bar.addView(browser,new LinearLayout.LayoutParams(0,-2,1));bar.addView(refresh,new LinearLayout.LayoutParams(0,-2,.65f));root.addView(bar);
  TextView note=new TextView(this);note.setText("原作者完整网页 · 需要联网 · 不是完整中文翻译\n网页有英文时，可在浏览器使用翻译；返回不会重置教程进度。");note.setTextColor(Color.LTGRAY);note.setTextSize(12);note.setPadding(16,8,16,10);root.addView(note);
  page=new WebView(this);WebSettings settings=page.getSettings();settings.setJavaScriptEnabled(true);settings.setDomStorageEnabled(true);settings.setAllowFileAccess(false);settings.setAllowContentAccess(false);settings.setAllowFileAccessFromFileURLs(false);settings.setAllowUniversalAccessFromFileURLs(false);settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);settings.setBuiltInZoomControls(true);settings.setDisplayZoomControls(false);
  page.setWebViewClient(new WebViewClient(){@Override public boolean shouldOverrideUrlLoading(WebView w,WebResourceRequest r){if(trusted(r.getUrl())){currentUrl=r.getUrl().toString();return false;}if("https".equalsIgnoreCase(r.getUrl().getScheme()))openExternal(r.getUrl());return true;}@Override public void onReceivedError(WebView w,WebResourceRequest r,WebResourceError e){if(r.isForMainFrame())note.setText("原文网页加载失败，请检查网络后刷新，或用浏览器打开。离线地图和本地教程仍可使用。");}});
  root.addView(page,new LinearLayout.LayoutParams(-1,0,1));setContentView(root);root.requestApplyInsets();page.loadUrl(currentUrl);
 }
 private void openExternal(Uri uri){try{startActivity(new Intent(Intent.ACTION_VIEW,uri));}catch(android.content.ActivityNotFoundException ignored){}}
 @Override public void onBackPressed(){if(page!=null&&page.canGoBack())page.goBack();else finish();}
 @Override protected void onDestroy(){if(page!=null){page.destroy();page=null;}super.onDestroy();}
}
