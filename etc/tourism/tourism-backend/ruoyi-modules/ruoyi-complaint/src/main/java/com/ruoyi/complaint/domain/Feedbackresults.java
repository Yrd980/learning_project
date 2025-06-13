package com.ruoyi.complaint.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 投诉处理反馈信息对象 feedbackresults
 * 
 * @author ningf
 * @date 2024-07-15
 */
public class Feedbackresults extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 反馈id */
    private Long id;

    /** 处理结果id */
    @Excel(name = "处理结果id")
    private Long handleResultId;

    /** 评分 */
    @Excel(name = "评分")
    private Long rating;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setHandleResultId(Long handleResultId) 
    {
        this.handleResultId = handleResultId;
    }

    public Long getHandleResultId() 
    {
        return handleResultId;
    }
    public void setRating(Long rating) 
    {
        this.rating = rating;
    }

    public Long getRating() 
    {
        return rating;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("handleResultId", getHandleResultId())
            .append("rating", getRating())
            .toString();
    }
}
