#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <algorithm>
#include <sstream>
#include <curl/curl.h>
#include <myo/myo.hpp>
using namespace std;
class DataCollector : public myo::DeviceListener {
public:
    DataCollector()
    : onArm(false), isUnlocked(false), roll_w(0), pitch_w(0), yaw_w(0), currentPose()
    {
    }
    
    // onUnpair() is called whenever the Myo is disconnected from Myo Connect by the user.
    void onUnpair(myo::Myo* myo, uint64_t timestamp)
    {
        // We've lost a Myo.
        // Let's clean up some leftover state.
        roll_w = 0;
        pitch_w = 0;
        yaw_w = 0;
        onArm = false;
        isUnlocked = false;
    }
    
    // onOrientationData() is called whenever the Myo device provides its current orientation, which is represented
    // as a unit quaternion.
    void onOrientationData(myo::Myo* myo, uint64_t timestamp, const myo::Quaternion<float>& quat)
    {
        using std::atan2;
        using std::asin;
        using std::sqrt;
        using std::max;
        using std::min;
        
        // Calculate Euler angles (roll, pitch, and yaw) from the unit quaternion.
        float roll = atan2(2.0f * (quat.w() * quat.x() + quat.y() * quat.z()),
                           1.0f - 2.0f * (quat.x() * quat.x() + quat.y() * quat.y()));
        float pitch = asin(max(-1.0f, min(1.0f, 2.0f * (quat.w() * quat.y() - quat.z() * quat.x()))));
        float yaw = atan2(2.0f * (quat.w() * quat.z() + quat.x() * quat.y()),
                          1.0f - 2.0f * (quat.y() * quat.y() + quat.z() * quat.z()));
        
        // Convert the floating point angles in radians to a scale from 0 to 18.
        roll_w = static_cast<int>((roll + (float)M_PI)/(M_PI * 2.0f) * 18);
        pitch_w = static_cast<int>((pitch + (float)M_PI/2.0f)/M_PI * 18);
        yaw_w = static_cast<int>((yaw + (float)M_PI)/(M_PI * 2.0f) * 18);
    }
    
    // onPose() is called whenever the Myo detects that the person wearing it has changed their pose, for example,
    // making a fist, or not making a fist anymore.
    void onPose(myo::Myo* myo, uint64_t timestamp, myo::Pose pose)
    {
        currentPose = pose;
        
        if (pose != myo::Pose::unknown && pose != myo::Pose::rest) {
            // Tell the Myo to stay unlocked until told otherwise. We do that here so you can hold the poses without the
            // Myo becoming locked.
            myo->unlock(myo::Myo::unlockHold);
            
            // Notify the Myo that the pose has resulted in an action, in this case changing
            // the text on the screen. The Myo will vibrate.
            myo->notifyUserAction();
        } else {
            // Tell the Myo to stay unlocked only for a short period. This allows the Myo to stay unlocked while poses
            // are being performed, but lock after inactivity.
            myo->unlock(myo::Myo::unlockTimed);
        }
    }
    
    // onArmSync() is called whenever Myo has recognized a Sync Gesture after someone has put it on their
    // arm. This lets Myo know which arm it's on and which way it's facing.
    void onArmSync(myo::Myo* myo, uint64_t timestamp, myo::Arm arm, myo::XDirection xDirection)
    {
        onArm = true;
        whichArm = arm;
    }
    
    // onArmUnsync() is called whenever Myo has detected that it was moved from a stable position on a person's arm after
    // it recognized the arm. Typically this happens when someone takes Myo off of their arm, but it can also happen
    // when Myo is moved around on the arm.
    void onArmUnsync(myo::Myo* myo, uint64_t timestamp)
    {
        onArm = false;
    }
    
    // onUnlock() is called whenever Myo has become unlocked, and will start delivering pose events.
    void onUnlock(myo::Myo* myo, uint64_t timestamp)
    {
        isUnlocked = true;
    }
    
    // onLock() is called whenever Myo has become locked. No pose events will be sent until the Myo is unlocked again.
    void onLock(myo::Myo* myo, uint64_t timestamp)
    {
        isUnlocked = false;
    }
    
    // There are other virtual functions in DeviceListener that we could override here, like onAccelerometerData().
    // For this example, the functions overridden above are sufficient.
    
    // We define this function to print the current values that were updated by the on...() functions above.
    int print()
    {
        // Clear the current line
        std::cout << '\r';
        
        /*// Print out the orientation. Orientation data is always available, even if no arm is currently recognized.
        std::cout << '[' << std::string(roll_w, '*') << std::string(18 - roll_w, ' ') << ']'
        << '[' << std::string(pitch_w, '*') << std::string(18 - pitch_w, ' ') << ']'
        << '[' << std::string(yaw_w, '*') << std::string(18 - yaw_w, ' ') << ']';
        
         //--------------------------------------------
        if (onArm) {
            // Print out the lock state, the currently recognized pose, and which arm Myo is being worn on.
            
            // Pose::toString() provides the human-readable name of a pose. We can also output a Pose directly to an
            // output stream (e.g. std::cout << currentPose;). In this case we want to get the pose name's length so
            // that we can fill the rest of the field with spaces below, so we obtain it as a string using toString().
            std::string poseString = currentPose.toString();
            
            std::cout << '[' << (isUnlocked ? "unlocked" : "locked  ") << ']'
            << '[' << (whichArm == myo::armLeft ? "L" : "R") << ']'
            << '[' << poseString << std::string(14 - poseString.size(), ' ') << ']';
        } else {
            // Print out a placeholder for the arm and pose when Myo doesn't currently know which arm it's on.
            std::cout << '[' << std::string(8, ' ') << ']' << "[?]" << '[' << std::string(14, ' ') << ']';
        }*/
        //------------------------------------------------
        
        cout<<"Volume: "<<(18-pitch_w);
        cout << std::flush;
        return (18-pitch_w);
    }
    
    // These values are set by onArmSync() and onArmUnsync() above.
    bool onArm;
    myo::Arm whichArm;
    
    // This is set by onUnlocked() and onLocked() above.
    bool isUnlocked;
    
    // These values are set by onOrientationData() and onPose() above.
    int roll_w, pitch_w, yaw_w;
    
    myo::Pose currentPose;
    
    
};

void clearDatabase(){                   //This function is called to RESET the databse at the beginning of every session
    CURL *curl;
    CURLcode res;
    
    struct curl_slist *headerlist=NULL;     
    static const char buf[] = "Expect:";
    
    curl_global_init(CURL_GLOBAL_ALL);
    
    curl = curl_easy_init();
    
    headerlist = curl_slist_append(headerlist, buf);
    if(curl) {
        
        curl_easy_setopt(curl, CURLOPT_URL, "104.237.150.7/cleardb.php");
      
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headerlist);
        
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "clear=true");
        
        res = curl_easy_perform(curl);
       
        if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        curl_slist_free_all (headerlist);
    }
    cout<<"DB CLEARED!";
}

int main(int argc, char** argv)
{
    
    int volume = 0;
    
    // We catch any exceptions that might occur below -- see the catch statement for more details.
    try {
        
        myo::Hub hub("com.myo.penn");
        std::cout << "Attempting to find a Myo..." << std::endl;
        myo::Myo* myo = hub.waitForMyo(10000);
    
        if (!myo) {
            throw std::runtime_error("Unable to find a Myo!");
        }
        
        //Found a Myo.
        std::cout << "Connected to a Myo armband!" << std::endl << std::endl;
    
        DataCollector collector;
        
        hub.addListener(&collector);
        
        clearDatabase();                        //Calling clearDatabase() to reset database at the beginning of every session
        
     
        while (1) {
            // We wish to update our display 20 times a second, so we run for 1000/20 milliseconds.
            hub.run(1000/20);
            volume = collector.print();
            stringstream strs;
            strs << volume;
            string temp_str = strs.str();
            
            char* post_data = "vertical=";
            
            size_t len = strlen(post_data);
            
            char* ret = (char*) temp_str.c_str();
           
            char result[20];
            strcpy(result,post_data);
            strcat(result,ret);
            
            CURL *curl;
            CURLcode res;
            
            struct curl_httppost *formpost=NULL;
         
            struct curl_slist *headerlist=NULL;
            static const char buf[] = "Expect:";
            
            curl_global_init(CURL_GLOBAL_ALL);
            
            curl = curl_easy_init();
            /* initalize custom header list (stating that Expect: 100-continue is not
             wanted */
            headerlist = curl_slist_append(headerlist, buf);
            if(curl) {
                curl_easy_setopt(curl, CURLOPT_URL, "104.237.150.7/control.php");
                if ( (argc == 2) && (!strcmp(argv[1], "noexpectheader")) )
                
                curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headerlist);
                
                curl_easy_setopt(curl, CURLOPT_POSTFIELDS, result);
                
                /* Perform the request, res will get the return code */
                res = curl_easy_perform(curl);
                /* Check for errors */
                if(res != CURLE_OK)
                fprintf(stderr, "curl_easy_perform() failed: %s\n",
                        curl_easy_strerror(res));
                
                /* always cleanup */
                curl_easy_cleanup(curl);
                
                /* then cleanup the formpost chain */ 
                curl_formfree(formpost);
                /* free slist */ 
                curl_slist_free_all (headerlist);
            }
        }
        
        // If a standard exception occurred, we print out its message and exit.
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cerr << "Press enter to continue.";
        std::cin.ignore();
        return 1;
    }
}
