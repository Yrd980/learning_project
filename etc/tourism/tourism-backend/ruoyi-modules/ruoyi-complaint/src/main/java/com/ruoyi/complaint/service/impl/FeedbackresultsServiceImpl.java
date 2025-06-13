package com.ruoyi.complaint.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.complaint.mapper.FeedbackresultsMapper;
import com.ruoyi.complaint.domain.Feedbackresults;
import com.ruoyi.complaint.service.IFeedbackresultsService;

/**
 * 投诉处理反馈信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-15
 */
@Service
public class FeedbackresultsServiceImpl implements IFeedbackresultsService 
{
    @Autowired
    private FeedbackresultsMapper feedbackresultsMapper;

    /**
     * 查询投诉处理反馈信息
     * 
     * @param id 投诉处理反馈信息主键
     * @return 投诉处理反馈信息
     */
    @Override
    public Feedbackresults selectFeedbackresultsById(Long id)
    {
        return feedbackresultsMapper.selectFeedbackresultsById(id);
    }

    /**
     * 查询投诉处理反馈信息列表
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 投诉处理反馈信息
     */
    @Override
    public List<Feedbackresults> selectFeedbackresultsList(Feedbackresults feedbackresults)
    {
        return feedbackresultsMapper.selectFeedbackresultsList(feedbackresults);
    }

    /**
     * 新增投诉处理反馈信息
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 结果
     */
    @Override
    public int insertFeedbackresults(Feedbackresults feedbackresults)
    {
        return feedbackresultsMapper.insertFeedbackresults(feedbackresults);
    }

    /**
     * 修改投诉处理反馈信息
     * 
     * @param feedbackresults 投诉处理反馈信息
     * @return 结果
     */
    @Override
    public int updateFeedbackresults(Feedbackresults feedbackresults)
    {
        return feedbackresultsMapper.updateFeedbackresults(feedbackresults);
    }

    /**
     * 批量删除投诉处理反馈信息
     * 
     * @param ids 需要删除的投诉处理反馈信息主键
     * @return 结果
     */
    @Override
    public int deleteFeedbackresultsByIds(Long[] ids)
    {
        return feedbackresultsMapper.deleteFeedbackresultsByIds(ids);
    }

    /**
     * 删除投诉处理反馈信息信息
     * 
     * @param id 投诉处理反馈信息主键
     * @return 结果
     */
    @Override
    public int deleteFeedbackresultsById(Long id)
    {
        return feedbackresultsMapper.deleteFeedbackresultsById(id);
    }
}
