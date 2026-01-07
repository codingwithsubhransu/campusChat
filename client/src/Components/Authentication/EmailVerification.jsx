import React, { useEffect, useState } from "react";

const EmailVerification = () => {
  const [otp, setOtp] = useState("");
  const [timeLeft, setTimeLeft] = useState(60);
  const [isResending, setIsResending] = useState(false);

  // Countdown timer
  useEffect(() => {
    if (timeLeft === 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const handleResend = () => {
    setIsResending(true);

    // simulate API call
    setTimeout(() => {
      setTimeLeft(60);
      setIsResending(false);
    }, 1500);
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-2xl rounded-xl shadow-lg p-8 space-y-6">
        
        {/* App Name */}
        <h1 className="text-4xl font-bold text-center text-green-600">
          campusChat
        </h1>

        {/* Heading */}
        <h2 className="text-2xl font-semibold text-gray-800 text-center">
          Verify your email to continue chatting seamlessly
        </h2>

        {/* Instruction */}
        <p className="text-gray-600 text-center">
          Enter the 6-digit verification code sent to your email.
        </p>

        {/* OTP Input */}
        <input
          type="text"
          maxLength={6}
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          placeholder="Enter 6-digit code"
          className="w-full p-4 text-2xl text-center tracking-widest border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
        />

        {/* Verify Button */}
        <button
          className="w-full bg-green-600 hover:bg-green-700 text-white py-4 text-xl font-semibold rounded-lg transition"
        >
          Verify
        </button>

        {/* Resend Section */}
        <div className="text-center text-gray-600">
          {timeLeft > 0 ? (
            <p className="text-xl">
              Resend code in{" "}
              <span className="font-semibold text-green-600">
                {timeLeft}s
              </span>
            </p>
          ) : (
            <button
              onClick={handleResend}
              disabled={isResending}
              className="text-green-600 font-semibold hover:underline disabled:opacity-50 text-2xl"
            >
              {isResending ? "Resending..." : "Resend Code"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmailVerification;
