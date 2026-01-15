import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "secondary" | "destructive" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
    const variants = {
        default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80 bg-blue-600 text-white",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80 bg-gray-100 text-gray-800",
        destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground border-gray-200 border",
    }
    return (
        <div className={cn("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2", variants[variant], className)} {...props} />
    )
}

export { Badge }
