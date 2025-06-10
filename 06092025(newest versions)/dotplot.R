# 加载包
library(ggplot2)
library(readr)
library(dplyr)
library(patchwork)
library(rlang)

# ✅ 参数设置：只改这里即可
xvar <- "PowerDensity"
fillvar <- "Mean_Value"
sizevar <- "Ratio"

# 读取数据
df1 <- read_csv("/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/DMPAG_FAM_删除自荧光/new qualification/Output_summary_level_5.csv")  
df2 <- read_csv("/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/DMPAG_Cy3_删除自荧光/Output_summary_level_5.csv")  

# Step 1: 构建完整 Region 顺序
region_df1_order <- df1 %>% arrange(!!sym(xvar)) %>% pull(Region)
region_df2_extra <- setdiff(df2$Region, df1$Region)
region_all <- c(sort(region_df2_extra),region_df1_order)

# Step 2: 用完整 Region 表 left_join 原始数据，补齐缺失区域
df1_full <- data.frame(Region = region_all) %>%
  left_join(df1, by = "Region") %>%
  mutate(Region = factor(Region, levels = region_all))

df2_full <- data.frame(Region = region_all) %>%
  left_join(df2, by = "Region") %>%
  mutate(Region = factor(Region, levels = region_all))

# Step 3: 统一色阶、大小、横坐标范围
fill_range <- range(c(df1_full[[fillvar]], df2_full[[fillvar]]), na.rm = TRUE)
size_range <- range(c(df1_full[[sizevar]], df2_full[[sizevar]]), na.rm = TRUE)
x_range <- range(c(df1_full[[xvar]], df2_full[[xvar]]), na.rm = TRUE)
x_breaks <- seq(floor(x_range[1]), ceiling(x_range[2]), by = 100)

# Step 4: 公共主题
common_theme <- theme_bw() +
  theme(
    axis.title.y = element_blank(),
    axis.text.y = element_text(size = 10, color = "black"),
    axis.text.x = element_text(size = 10),
    panel.grid.major = element_line(color = "grey85"),
    panel.grid.minor = element_blank(),
    panel.border = element_rect(color = "black", fill = NA),
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 9),
    legend.key.size = unit(0.5, "cm")
  )

# Step 5: 图1（左，FITC）
p1 <- ggplot(df1_full, aes(x = !!sym(xvar), y = Region)) +
  geom_point(aes(size = !!sym(sizevar)), fill = "black", shape = 21, color = "black",
             stroke = 0.3, alpha = 0.6, na.rm = TRUE) +
  geom_point(aes(size = !!sym(sizevar), fill = !!sym(fillvar)), shape = 21, color = "black",
             stroke = 0.3, na.rm = TRUE) +
  scale_fill_gradient(low = "#0571b0", high = "#ca0020", limits = fill_range) +
  scale_size_continuous(range = c(3, 15), limits = size_range,
                        guide = guide_legend(reverse = TRUE)) +
  scale_x_continuous(limits = x_range, breaks = x_breaks) +
  common_theme +
  theme(plot.margin = margin(5, 5, 5, 20)) +
  labs(x = "FITC", size = sizevar, fill = fillvar)

# Step 6: 图2（右，Cy3）
p2 <- ggplot(df2_full, aes(x = !!sym(xvar), y = Region)) +
  geom_point(aes(size = !!sym(sizevar)), fill = "black", shape = 21, color = "black",
             stroke = 0.3, alpha = 0.6, na.rm = TRUE) +
  geom_point(aes(size = !!sym(sizevar), fill = !!sym(fillvar)), shape = 21, color = "black",
             stroke = 0.3, na.rm = TRUE) +
  scale_fill_gradient(low = "#0571b0", high = "#ca0020", limits = fill_range) +
  scale_size_continuous(range = c(3, 15), limits = size_range,
                        guide = guide_legend(reverse = TRUE)) +
  scale_x_continuous(limits = x_range, breaks = x_breaks) +
  common_theme +
  theme(
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    plot.margin = margin(5, 20, 5, 5)
  ) +
  labs(x = "Cy3", size = sizevar, fill = fillvar)

# Step 7: 拼接图形，合并图例
combined_plot <- p1 + p2 + plot_layout(ncol = 2, guides = "collect")

# 显示图形
print(combined_plot)

# 保存（可选）
ggsave("/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/Dotplot.png",
       plot = combined_plot, width = 12, height = 10, dpi = 300)
