package course.labs.locationlab;

import java.util.ArrayList;

import android.app.ListActivity;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Toast;

public class PlaceViewActivity extends ListActivity implements LocationListener {
	private static final long FIVE_MINS = 5 * 60 * 1000;

	private static String TAG = "Lab-Location";

	// The last valid location reading
	private Location mLastLocationReading;

	// The ListView's adapter
	private PlaceViewAdapter mAdapter;

	// default minimum time between new location readings
	private long mMinTime = 5000;

	// default minimum distance between old and new readings.
	private float mMinDistance = 1000.0f;

	// Reference to the LocationManager
	private LocationManager mLocationManager;

	// A fake location provider used for testing
	private MockLocationProvider mMockLocationProvider;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		mLocationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        if (mLocationManager == null) {
            finish();
        }
        
		mAdapter = new PlaceViewAdapter(this);
		View footer = LayoutInflater.from(this).inflate(R.layout.footer_view, null);
		
		getListView().addFooterView(footer);
		setListAdapter(mAdapter);

		footer.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v) {
				log("Entered footerView.OnClickListener.onClick()");
				if (mLastLocationReading == null) {
					log("Location data is not available");	
				} else if (!mAdapter.intersects(mLastLocationReading)) {
					log("Starting Place Download");
					new PlaceDownloaderTask(PlaceViewActivity.this)
						.execute(mLastLocationReading);
				} else {
					Toast
						.makeText(PlaceViewActivity.this, "You already have this location badge", Toast.LENGTH_LONG)
						.show();
					log("You already have this location badge");
				}
			}
		});
	}

	@Override
	protected void onResume() {
		super.onResume();
		
		mMockLocationProvider = new MockLocationProvider(LocationManager.NETWORK_PROVIDER, this);
		Location location = mLocationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
		if (location != null && age(location) < FIVE_MINS) {
			mLastLocationReading = location;
		}
		mLocationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, mMinTime, mMinDistance, this);
	}

	@Override
	protected void onPause() {

		mMockLocationProvider.shutdown();
		mLocationManager.removeUpdates(this);
		super.onPause();
	}

	public void addNewPlace(PlaceRecord place) {

		log("Entered addNewPlace()");
		mAdapter.add(place);
	}

	@Override
	public void onLocationChanged(Location currentLocation) {
		if ((mLastLocationReading == null)
		 || (currentLocation.getTime() > mLastLocationReading.getTime())) {
			mLastLocationReading = currentLocation;
		}
	}

	@Override
	public void onProviderDisabled(String provider) {
		// not implemented
	}

	@Override
	public void onProviderEnabled(String provider) {
		// not implemented
	}

	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// not implemented
	}

	private long age(Location location) {
		return System.currentTimeMillis() - location.getTime();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case R.id.print_badges:
			ArrayList<PlaceRecord> currData = mAdapter.getList();
			for (int i = 0; i < currData.size(); i++) {
				log(currData.get(i).toString());
			}
			return true;
		case R.id.delete_badges:
			mAdapter.removeAllViews();
			return true;
		case R.id.place_one:
			mMockLocationProvider.pushLocation(37.422, -122.084);
			return true;
		case R.id.place_invalid:
			mMockLocationProvider.pushLocation(0, 0);
			return true;
		case R.id.place_two:
			mMockLocationProvider.pushLocation(38.996667, -76.9275);
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}

	private static void log(String msg) {
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		Log.i(TAG, msg);
	}
}
