'use client'
import type { FC } from 'react'
import useTheme from '@/hooks/use-theme'
import { cn } from '@/utils/classnames'
import { basePath } from '@/utils/var'

export type LogoStyle = 'default' | 'monochromeWhite'

export const logoPathMap: Record<LogoStyle, string> = {
  default: '/logo/logo.svg',
  monochromeWhite: '/logo/logo-monochrome-white.svg',
}

export type LogoSize = 'large' | 'medium' | 'small'

export const logoSizeMap: Record<LogoSize, string> = {
  large: 'w-16 h-7',
  medium: 'w-12 h-[22px]',
  small: 'w-9 h-4',
}

type DifyLogoProps = {
  style?: LogoStyle
  size?: LogoSize
  className?: string
}

const DifyLogo: FC<DifyLogoProps> = ({
  style = 'default',
  size = 'medium',
  className,
}) => {
  const { theme } = useTheme()
  const isWhite = (theme === 'dark' && style === 'default') || style === 'monochromeWhite'

  // Font size mapping based on logo size
  const fontSizeMap: Record<LogoSize, string> = {
    large: 'text-lg font-semibold',
    medium: 'text-base font-semibold',
    small: 'text-sm font-semibold',
  }

  return (
    <span
      className={cn(
        'block font-semibold',
        fontSizeMap[size],
        isWhite ? 'text-white' : 'text-gray-900',
        className
      )}
    >
      BlueData
    </span>
  )
}

export default DifyLogo
