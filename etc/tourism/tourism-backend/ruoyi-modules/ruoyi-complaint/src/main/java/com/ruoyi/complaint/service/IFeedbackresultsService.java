package com.ruoyi.complaint.service;

import java.util.List;
import com.ruoyi.complaint.domain.Feedbackresults;

/**
 * 投诉处理反馈信息Service接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface IFeedbackresultsService 
{
    /**
     * 查询投诉处理反馈信息
     * 
     * @param id 投诉处理反馈信息主键
     * @return 投诉处理反馈信息
     */
    public Feedbackresults selectFeedbackresultsById(Long id);

    /**
     * 查询投诉处理反馈信息列表
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 投诉处理反馈信息集合
     */
    public List<Feedbackresults> selectFeedbackresultsList(Feedbackresults feedbackresults);

    /**
     * 新增投诉处理反馈信息
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 结果
     */
    public int insertFeedbackresults(Feedbackresults feedbackresults);

    /**
     * 修改投诉处理反馈信息
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 结果
     */
    public int updateFeedbackresults(Feedbackresults feedbackresults);

    /**
     * 批量删除投诉处理反馈信息
     * 
     * @param ids 需要删除的投诉处理反馈信息主键集合
     * @return 结果
     */
    public int deleteFeedbackresultsByIds(Long[] ids);

    /**
     * 删除投诉处理反馈信息信息
     * 
     * @param id 投诉处理反馈信息主键
     * @return 结果
     */
    public int deleteFeedbackresultsById(Long id);
}
