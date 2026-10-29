import { resend } from "@/lib/resend";
import VerificationEmail from "../../emails/VerificationEmail";
import { ApiResponse } from "@/types/ApiResponse";


export const sendVerificationEmail = async (email: string, username: string, verifyCode: string): Promise<ApiResponse> => {
    // Local development without a mail provider: the code is the console line.
    if (!process.env.RESEND_API_KEY) {
        console.info(`[local] verification code for ${email}: ${verifyCode}`);
        return { success: true, message: "Verification code printed to the server console" };
    }

    try {
        await resend.emails.send({
            from: 'onboarding@resend.dev',
            to: email,
            subject: "Leetcode-Clone (NEXT JS Project) Verification Code",
            react: VerificationEmail({username, otp: verifyCode})
        });
        
        return { success: true, message: "Verification email send successfully" };
    } catch (error) {
        console.error("Error sending verification email: ", error);
        return { success: false, message: "Failed to send verification email" }
    }
}