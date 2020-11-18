#include <iostream>
#include <chrono>
#include <ctime>
#include <cmath>

class Timer
{

    double totalElapsed = 0.f;

private:
    std::chrono::time_point<std::chrono::system_clock> m_StartTime;
    std::chrono::time_point<std::chrono::system_clock> m_EndTime;
    bool                                               m_bRunning = false;
    
public:
    void start()
    {
        m_StartTime = std::chrono::system_clock::now();
        m_bRunning = true;
    }
    
    void stop()
    {
        m_EndTime = std::chrono::system_clock::now();
        m_bRunning = false;
	totalElapsed = totalElapsed + std::chrono::duration_cast<std::chrono::milliseconds>(m_EndTime - m_StartTime).count();
    }
    
    double elapsedMilliseconds()
    {        
        return totalElapsed;
    }
    
    double elapsedSeconds()
    {
        return elapsedMilliseconds() / 1000.0;
    }

};

