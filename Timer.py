import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Volume2, VolumeX } from 'lucide-react';

export default function MeditationTimer() {
  const [duration, setDuration] = useState(5);
  const [timeLeft, setTimeLeft] = useState(duration * 60);
  const [isActive, setIsActive] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [sessionsCompleted, setSessionsCompleted] = useState(0);
  const audioContextRef = useRef(null);
  const oscillatorRef = useRef(null);
  const gainNodeRef = useRef(null);

  useEffect(() => {
    let interval = null;
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(time => time - 1);
      }, 1000);
    } else if (timeLeft === 0 && isActive) {
      setIsActive(false);
      setSessionsCompleted(prev => prev + 1);
      playCompletionSound();
    }
    return () => clearInterval(interval);
  }, [isActive, timeLeft]);

  useEffect(() => {
    setTimeLeft(duration * 60);
  }, [duration]);

  const toggleTimer = () => {
    setIsActive(!isActive);
    if (!isActive && soundEnabled) {
      startAmbientSound();
    } else {
      stopAmbientSound();
    }
  };

  const resetTimer = () => {
    setIsActive(false);
    setTimeLeft(duration * 60);
    stopAmbientSound();
  };

  const startAmbientSound = () => {
    if (!soundEnabled) return;

    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    oscillatorRef.current = audioContextRef.current.createOscillator();
    gainNodeRef.current = audioContextRef.current.createGain();

    oscillatorRef.current.type = 'sine';
    oscillatorRef.current.frequency.setValueAtTime(200, audioContextRef.current.currentTime);
    gainNodeRef.current.gain.setValueAtTime(0.03, audioContextRef.current.currentTime);

    oscillatorRef.current.connect(gainNodeRef.current);
    gainNodeRef.current.connect(audioContextRef.current.destination);
    oscillatorRef.current.start();
  };

  const stopAmbientSound = () => {
    if (oscillatorRef.current) {
      oscillatorRef.current.stop();
      oscillatorRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
  };

  const playCompletionSound = () => {
    if (!soundEnabled) return;

    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.frequency.setValueAtTime(528, ctx.currentTime);
    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 1);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = ((duration * 60 - timeLeft) / (duration * 60)) * 100;
  const circumference = 2 * Math.PI * 140;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-light text-gray-800 mb-2">Mindful Moments</h1>
            <p className="text-sm text-gray-500">Find your inner peace</p>
          </div>

          <div className="relative w-80 h-80 mx-auto mb-8">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="160"
                cy="160"
                r="140"
                stroke="#e5e7eb"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="160"
                cy="160"
                r="140"
                stroke="url(#gradient)"
                strokeWidth="8"
                fill="none"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-linear"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#818cf8" />
                  <stop offset="100%" stopColor="#c084fc" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl font-light text-gray-800 mb-2">
                  {formatTime(timeLeft)}
                </div>
                <div className="text-sm text-gray-500">
                  {isActive ? 'Breathe...' : 'Ready to begin'}
                </div>
              </div>
            </div>
          </div>

          {!isActive && (
            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-700 mb-3 text-center">
                Session Duration
              </label>
              <div className="flex gap-2 justify-center flex-wrap">
                {[2, 3, 5, 10, 15, 20, 60].map((min) => (
                  <button
                    key={min}
                    onClick={() => setDuration(min)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                      duration === min
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {min >= 60 ? `${min / 60}h` : `${min}m`}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center justify-center gap-4 mb-6">
            <button
              onClick={resetTimer}
              className="p-4 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              <RotateCcw className="w-5 h-5 text-gray-600" />
            </button>
            <button
              onClick={toggleTimer}
              className="p-6 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 shadow-lg transition-all transform hover:scale-105"
            >
              {isActive ? (
                <Pause className="w-8 h-8 text-white" />
              ) : (
                <Play className="w-8 h-8 text-white ml-1" />
              )}
            </button>
            <button
              onClick={() => {
                setSoundEnabled(!soundEnabled);
                if (isActive && soundEnabled) {
                  stopAmbientSound();
                } else if (isActive && !soundEnabled) {
                  startAmbientSound();
                }
              }}
              className="p-4 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              {soundEnabled ? (
                <Volume2 className="w-5 h-5 text-gray-600" />
              ) : (
                <VolumeX className="w-5 h-5 text-gray-600" />
              )}
            </button>
          </div>

          <div className="text-center pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Sessions completed today: <span className="font-semibold text-purple-600">{sessionsCompleted}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
