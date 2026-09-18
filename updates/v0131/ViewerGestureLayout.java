package com.openai.cod15guide;

import android.content.Context;
import android.view.MotionEvent;
import android.view.ViewConfiguration;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.widget.FrameLayout;

/** Single-finger horizontal paging before WebView consumes a zoomed-image drag.
 * The minimal mode bridge exists only on MainActivity's asset-backed WebView.
 * ReaderActivity never receives this bridge.
 */
public final class ViewerGestureLayout extends FrameLayout {
    private WebView webView;
    private volatile boolean viewerActive;
    private volatile boolean imagePan;
    private float startX, startY;
    private long startTime;
    private boolean tracking, horizontal, vertical, multiple;
    private final float slop, minDistance, fastDistance;
    public ViewerGestureLayout(Context context) {
        super(context);
        float density = getResources().getDisplayMetrics().density;
        slop = Math.max(ViewConfiguration.get(context).getScaledTouchSlop(), 10f * density);
        minDistance = 44f * density;
        fastDistance = 24f * density;
    }
    public void attach(WebView view) {
        webView = view;
        view.addJavascriptInterface(new ModeBridge(), "LocalViewerGesture");
    }
    public final class ModeBridge {
        @JavascriptInterface public void setMode(boolean active, boolean pan) {
            viewerActive = active;
            imagePan = pan;
        }
    }
    @Override public void requestDisallowInterceptTouchEvent(boolean disallow) {
        super.requestDisallowInterceptTouchEvent(disallow && (!viewerActive || imagePan || multiple));
    }
    @Override public boolean onInterceptTouchEvent(MotionEvent event) {
        if (!viewerActive || imagePan) { tracking = horizontal = false; return false; }
        switch (event.getActionMasked()) {
            case MotionEvent.ACTION_DOWN:
                startX = event.getX(); startY = event.getY(); startTime = event.getEventTime();
                tracking = true; horizontal = vertical = multiple = false;
                return false;
            case MotionEvent.ACTION_POINTER_DOWN:
                multiple = true; tracking = false;
                return horizontal;
            case MotionEvent.ACTION_MOVE:
                if (!tracking || multiple || event.getPointerCount() != 1 || vertical) return false;
                float dx = Math.abs(event.getX() - startX), dy = Math.abs(event.getY() - startY);
                if (dy > slop && dy > dx * 1.15f) { vertical = true; tracking = false; return false; }
                if (dx > slop && dx > dy * 1.25f) { horizontal = true; return true; }
                return false;
            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_CANCEL:
                tracking = false; return false;
            default: return horizontal;
        }
    }
    @Override public boolean onTouchEvent(MotionEvent event) {
        if (!horizontal) return super.onTouchEvent(event);
        if (event.getActionMasked() == MotionEvent.ACTION_POINTER_DOWN) multiple = true;
        if (event.getActionMasked() == MotionEvent.ACTION_UP) {
            float dx = event.getX() - startX, dy = event.getY() - startY;
            long duration = Math.max(1, event.getEventTime() - startTime);
            boolean distance = Math.abs(dx) >= minDistance || (duration < 280 && Math.abs(dx) >= fastDistance);
            boolean valid = viewerActive && !imagePan && !multiple && distance && Math.abs(dx) > Math.abs(dy) * 1.25f;
            horizontal = tracking = false;
            if (valid && webView != null) {
                final int direction = dx < 0 ? 1 : -1;
                webView.evaluateJavascript("window.guideViewerSwipe && window.guideViewerSwipe(" + direction + ")", null);
            }
            return true;
        }
        if (event.getActionMasked() == MotionEvent.ACTION_CANCEL) { horizontal = tracking = false; return true; }
        return true;
    }
}
